"""Core implementation of the Arc Memory SDK.

This module provides the `Arc` class, which is the main entry point for the SDK.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from arc_memory.db import get_adapter as get_db_adapter
from arc_memory.db.base import DatabaseAdapter
from arc_memory.errors import ArcError, DatabaseError
from arc_memory.schema.models import Edge, Node
from arc_memory.sql.db import ensure_arc_dir, get_db_path

from arc_memory.sdk.adapters import FrameworkAdapter, get_adapter, discover_adapters
from arc_memory.sdk.errors import SDKError, AdapterError, QueryError, BuildError, FrameworkError
from arc_memory.sdk.models import (
    DecisionTrailEntry, EntityDetails, HistoryEntry, ImpactResult, QueryResult, RelatedEntity,
    ExportResult
)
from arc_memory.sdk.progress import ProgressCallback


class Arc:
    """Main entry point for the Arc Memory SDK.

    This class provides methods for interacting with the Arc Memory knowledge graph.
    It is designed to be framework-agnostic, allowing integration with various agent
    frameworks through adapters.

    Attributes:
        repo_path: Path to the Git repository.
        adapter: Database adapter instance.
    """

    def __init__(
        self,
        repo_path: Union[str, Path],
        adapter_type: Optional[str] = None,
        connection_params: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the Arc Memory SDK.

        Args:
            repo_path: Path to the Git repository.
            adapter_type: Type of database adapter to use. If None, uses the configured adapter.
            connection_params: Parameters for connecting to the database.
                If None, uses default parameters.

        Raises:
            SDKError: If initialization fails.
            AdapterError: If the adapter cannot be initialized.
        """
        try:
            self.repo_path = Path(repo_path)

            # Get the database adapter
            self.adapter = get_db_adapter(adapter_type)

            # Connect to the database
            if not connection_params:
                # Use default connection parameters
                db_path = get_db_path()
                connection_params = {"db_path": str(db_path)}

            # Connect to the database
            self.adapter.connect(connection_params)

            # Initialize the database schema if needed
            if not self.adapter.is_connected():
                raise AdapterError("Failed to connect to the database")

            # Initialize the database schema
            self.adapter.init_db()

            # Set current repository context
            self.current_repo_id = None

            # Initialize active repositories list (for multi-repo support)
            self.active_repos = []

            # Discover and register framework adapters
            discover_adapters()

        except DatabaseError as e:
            # Convert database errors to SDK errors
            raise AdapterError(f"Database adapter error: {e}", details=e.details) from e
        except Exception as e:
            # Convert other exceptions to SDK errors
            raise SDKError(f"Failed to initialize Arc Memory SDK: {e}") from e

    def is_graph_valid(self) -> bool:
        """Check if the knowledge graph exists and has the expected structure.

        This method verifies that:
        1. The database connection is active
        2. The required tables exist
        3. The schema version is compatible

        Returns:
            True if the graph is valid, False otherwise.
        """
        try:
            if not self.adapter.is_connected():
                return False

            # Check if required tables exist
            required_tables = ["nodes", "edges", "repositories"]
            for table in required_tables:
                cursor = self.adapter.conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table,)
                )
                if not cursor.fetchone():
                    return False

            # Check if nodes table has expected columns
            cursor = self.adapter.conn.execute("PRAGMA table_info(nodes)")
            columns = [row[1] for row in cursor.fetchall()]
            required_columns = ["id", "type", "title", "body", "repo_id"]
            for column in required_columns:
                if column not in columns:
                    return False

            return True
        except Exception:
            return False

    def get_graph_statistics(self) -> Dict[str, Any]:
        """Get statistics about the knowledge graph.

        This method provides insights into the size and composition of the graph,
        including counts of different node types, edge relationships, and repositories.

        Returns:
            Dictionary containing graph statistics.

        Raises:
            QueryError: If retrieving statistics fails.
        """
        try:
            if not self.adapter.is_connected():
                raise QueryError("Not connected to database")

            stats = {
                "total_nodes": 0,
                "total_edges": 0,
                "node_types": {},
                "edge_relationships": {},
                "repositories": [],
                "last_updated": None
            }

            # Get total node count
            cursor = self.adapter.conn.execute("SELECT COUNT(*) FROM nodes")
            stats["total_nodes"] = cursor.fetchone()[0]

            # Get node type distribution
            cursor = self.adapter.conn.execute(
                "SELECT type, COUNT(*) FROM nodes GROUP BY type"
            )
            for row in cursor.fetchall():
                stats["node_types"][row[0]] = row[1]

            # Get total edge count
            cursor = self.adapter.conn.execute("SELECT COUNT(*) FROM edges")
            stats["total_edges"] = cursor.fetchone()[0]

            # Get edge relationship distribution
            cursor = self.adapter.conn.execute(
                "SELECT rel, COUNT(*) FROM edges GROUP BY rel"
            )
            for row in cursor.fetchall():
                stats["edge_relationships"][row[0]] = row[1]

            # Get repository information
            repos = self.list_repositories()
            stats["repositories"] = repos

            # Get last updated timestamp
            cursor = self.adapter.conn.execute(
                "SELECT MAX(timestamp) FROM nodes"
            )
            last_updated = cursor.fetchone()[0]
            if last_updated:
                from datetime import datetime
                try:
                    stats["last_updated"] = datetime.fromisoformat(last_updated)
                except ValueError:
                    stats["last_updated"] = last_updated

            return stats
        except Exception as e:
            raise QueryError(f"Failed to get graph statistics: {e}") from e

    def _get_repo_id_from_path(self, path: Path) -> str:
        """Generate repository ID from path.

        Args:
            path: Path to the repository.

        Returns:
            Repository ID in the format "repository:{md5_hash}".

        Note:
            The path is normalized (converted to lowercase) before hashing to ensure
            consistency across different operating systems, especially those with
            case-insensitive file systems.
        """
        import hashlib
        # Normalize the path (convert to lowercase for case-insensitive consistency)
        normalized_path = str(path.absolute()).lower()
        return f"repository:{hashlib.md5(normalized_path.encode()).hexdigest()}"

    def ensure_repository(self, name: Optional[str] = None) -> str:
        """Ensure a repository entry exists for the current repo_path.

        This method checks if a repository entry exists for the current repo_path,
        and creates one if it doesn't. It returns the repository ID.

        Args:
            name: Optional name for the repository. If None, uses the repo_path name.

        Returns:
            The repository ID.

        Raises:
            QueryError: If ensuring the repository fails.
        """
        try:
            # Check if repository already exists
            repo = self.get_current_repository()
            if repo:
                self.current_repo_id = repo["id"]

                # Add to active repositories if not already there
                if self.current_repo_id not in self.active_repos:
                    self.active_repos.append(self.current_repo_id)

                return repo["id"]

            # Generate repository name from path if not provided
            if not name:
                name = self.repo_path.name

            # Generate repository ID (use path hash for deterministic IDs)
            repo_id = self._get_repo_id_from_path(self.repo_path)

            # Get repository URL from git config if available
            url = None
            try:
                import subprocess
                result = subprocess.run(
                    ["git", "-C", str(self.repo_path), "config", "--get", "remote.origin.url"],
                    capture_output=True, text=True, check=False
                )
                if result.returncode == 0:
                    url = result.stdout.strip()
            except Exception:
                pass

            # Get default branch
            default_branch = "main"
            try:
                result = subprocess.run(
                    ["git", "-C", str(self.repo_path), "symbolic-ref", "--short", "HEAD"],
                    capture_output=True, text=True, check=False
                )
                if result.returncode == 0:
                    default_branch = result.stdout.strip()
            except Exception:
                pass

            # Create repository node
            from arc_memory.schema.models import RepositoryNode
            repo_node = RepositoryNode(
                id=repo_id,
                title=name,
                name=name,
                url=url,
                local_path=str(self.repo_path.absolute()),
                default_branch=default_branch
            )

            # Add repository to database
            self.add_nodes_and_edges([repo_node], [])

            # Add to repositories table
            self.adapter.conn.execute(
                """
                INSERT OR REPLACE INTO repositories(id, name, url, local_path, default_branch)
                VALUES(?, ?, ?, ?, ?)
                """,
                (
                    repo_id,
                    name,
                    url,
                    str(self.repo_path.absolute()),
                    default_branch
                )
            )
            self.adapter.conn.commit()

            # Set current repository ID
            self.current_repo_id = repo_id

            # Add to active repositories
            if repo_id not in self.active_repos:
                self.active_repos.append(repo_id)

            return repo_id
        except Exception as e:
            raise QueryError(f"Failed to ensure repository: {e}") from e

    def get_current_repository(self) -> Optional[Dict[str, Any]]:
        """Get the current repository based on repo_path.

        Returns:
            The repository as a dictionary, or None if it doesn't exist.

        Raises:
            QueryError: If getting the repository fails.
        """
        try:
            # Execute query to find repository by local_path
            query = """
            SELECT * FROM repositories WHERE local_path = ?
            """
            params = (str(self.repo_path.absolute()),)

            # Execute query
            cursor = self.adapter.conn.execute(query, params)
            row = cursor.fetchone()

            if row is None:
                return None

            # Convert row to dictionary
            repo = dict(row)

            # Parse metadata if it exists
            if repo.get("metadata"):
                import json
                repo["metadata"] = json.loads(repo["metadata"])

            return repo
        except Exception as e:
            raise QueryError(f"Failed to get current repository: {e}") from e

    def list_repositories(self) -> List[Dict[str, Any]]:
        """List all repositories in the knowledge graph.

        Returns:
            List of repository dictionaries.

        Raises:
            QueryError: If listing repositories fails.
        """
        try:
            # Execute query to get all repositories
            cursor = self.adapter.conn.execute("SELECT * FROM repositories")
            repos = [dict(row) for row in cursor.fetchall()]

            # Parse metadata if it exists
            for repo in repos:
                if repo.get("metadata"):
                    import json
                    repo["metadata"] = json.loads(repo["metadata"])

            return repos
        except Exception as e:
            raise QueryError(f"Failed to list repositories: {e}") from e

    def add_repository(self, repo_path: Union[str, Path], name: Optional[str] = None) -> str:
        """Add a repository to the knowledge graph.

        Args:
            repo_path: Path to the repository.
            name: Optional name for the repository. If None, uses the directory name.

        Returns:
            Repository ID.

        Raises:
            QueryError: If adding the repository fails.
        """
        try:
            # Convert to Path
            path = Path(repo_path)

            # Check if repository exists
            query = """
            SELECT id FROM repositories WHERE local_path = ?
            """
            params = (str(path.absolute()),)

            cursor = self.adapter.conn.execute(query, params)
            row = cursor.fetchone()

            if row:
                repo_id = row["id"]

                # Add to active repositories if not already there
                if repo_id not in self.active_repos:
                    self.active_repos.append(repo_id)

                return repo_id

            # Generate repository name from path if not provided
            if not name:
                name = path.name

            # Generate repository ID
            repo_id = self._get_repo_id_from_path(path)

            # Get repository URL from git config if available
            url = None
            try:
                import subprocess
                result = subprocess.run(
                    ["git", "-C", str(path), "config", "--get", "remote.origin.url"],
                    capture_output=True, text=True, check=False
                )
                if result.returncode == 0:
                    url = result.stdout.strip()
            except Exception:
                pass

            # Get default branch
            default_branch = "main"
            try:
                result = subprocess.run(
                    ["git", "-C", str(path), "symbolic-ref", "--short", "HEAD"],
                    capture_output=True, text=True, check=False
                )
                if result.returncode == 0:
                    default_branch = result.stdout.strip()
            except Exception:
                pass

            # Create repository node
            from arc_memory.schema.models import RepositoryNode
            repo_node = RepositoryNode(
                id=repo_id,
                title=name,
                name=name,
                url=url,
                local_path=str(path.absolute()),
                default_branch=default_branch
            )

            # Add repository to database
            self.add_nodes_and_edges([repo_node], [])

            # Add to repositories table
            self.adapter.conn.execute(
                """
                INSERT OR REPLACE INTO repositories(id, name, url, local_path, default_branch)
                VALUES(?, ?, ?, ?, ?)
                """,
                (
                    repo_id,
                    name,
                    url,
                    str(path.absolute()),
                    default_branch
                )
            )
            self.adapter.conn.commit()

            # Add to active repositories
            if repo_id not in self.active_repos:
                self.active_repos.append(repo_id)

            return repo_id
        except Exception as e:
            raise QueryError(f"Failed to add repository: {e}") from e

    def set_active_repositories(self, repo_ids: List[str]) -> None:
        """Set the active repositories for queries.

        Args:
            repo_ids: List of repository IDs to use for queries.

        Raises:
            QueryError: If setting active repositories fails.
        """
        try:
            # Verify that all repository IDs exist
            for repo_id in repo_ids:
                cursor = self.adapter.conn.execute(
                    "SELECT id FROM repositories WHERE id = ?",
                    (repo_id,)
                )
                if not cursor.fetchone():
                    raise QueryError(f"Repository with ID {repo_id} does not exist")

            # Set active repositories
            self.active_repos = repo_ids.copy()
        except Exception as e:
            raise QueryError(f"Failed to set active repositories: {e}") from e

    def update_repository(
        self,
        repo_id: str,
        new_path: Optional[str] = None,
        new_name: Optional[str] = None,
        new_url: Optional[str] = None,
        new_default_branch: Optional[str] = None
    ) -> str:
        """Update repository information.

        Args:
            repo_id: The ID of the repository to update.
            new_path: New local path for the repository.
            new_name: New name for the repository.
            new_url: New URL for the repository.
            new_default_branch: New default branch for the repository.

        Returns:
            The repository ID (which may be new if path changed).

        Raises:
            QueryError: If the repository doesn't exist or cannot be updated.
        """
        if not self.adapter.is_connected():
            raise DatabaseError("Not connected to database")

        # Check if repository exists
        repos = self.list_repositories()
        repo = next((r for r in repos if r["id"] == repo_id), None)

        if not repo:
            raise QueryError(f"Repository with ID '{repo_id}' does not exist")

        try:
            # Start a transaction
            self.adapter.conn.execute("BEGIN TRANSACTION")

            # If path is changing, we need to generate a new ID
            new_repo_id = repo_id
            if new_path:
                path = Path(new_path)
                if not path.exists():
                    raise QueryError(f"Path does not exist: {new_path}")

                # Generate new repository ID
                new_repo_id = self._get_repo_id_from_path(path)

                # Check if a repository with this path already exists
                if new_repo_id != repo_id and any(r["id"] == new_repo_id for r in repos):
                    raise QueryError(f"A repository with this path already exists: {new_path}")

                # Update nodes to use new repo_id
                self.adapter.conn.execute(
                    "UPDATE nodes SET repo_id = ? WHERE repo_id = ?",
                    (new_repo_id, repo_id)
                )

                # Update active repositories list
                if repo_id in self.active_repos:
                    self.active_repos.remove(repo_id)
                    self.active_repos.append(new_repo_id)

                # If this is the current repository, update current_repo_id
                if self.current_repo_id == repo_id:
                    self.current_repo_id = new_repo_id

            # Update repository information
            update_fields = []
            params = []

            if new_path:
                update_fields.append("local_path = ?")
                params.append(str(Path(new_path).absolute()))

            if new_name:
                update_fields.append("name = ?")
                params.append(new_name)

            if new_url:
                update_fields.append("url = ?")
                params.append(new_url)

            if new_default_branch:
                update_fields.append("default_branch = ?")
                params.append(new_default_branch)

            if update_fields:
                # Add repo_id to params
                params.append(repo_id)

                # Update repository
                self.adapter.conn.execute(
                    f"UPDATE repositories SET {', '.join(update_fields)} WHERE id = ?",
                    tuple(params)
                )

            # If ID changed, we need to insert a new record and delete the old one
            if new_repo_id != repo_id:
                # Get updated repository info
                cursor = self.adapter.conn.execute(
                    "SELECT name, url, local_path, default_branch, created_at, metadata FROM repositories WHERE id = ?",
                    (repo_id,)
                )
                row = cursor.fetchone()

                if row:
                    # Insert new repository record
                    self.adapter.conn.execute(
                        """
                        INSERT INTO repositories(id, name, url, local_path, default_branch, created_at, metadata)
                        VALUES(?, ?, ?, ?, ?, ?, ?)
                        """,
                        (new_repo_id, row[0], row[1], row[2], row[3], row[4], row[5])
                    )

                    # Also update the repository node ID if it exists
                    from arc_memory.schema.models import NodeType
                    self.adapter.conn.execute(
                        "UPDATE nodes SET id = ? WHERE id = ? AND type = ?",
                        (new_repo_id, repo_id, NodeType.REPOSITORY.value)
                    )

                    # Delete old repository record
                    self.adapter.conn.execute(
                        "DELETE FROM repositories WHERE id = ?",
                        (repo_id,)
                    )

            # Commit transaction
            self.adapter.conn.commit()
            return new_repo_id

        except Exception as e:
            # Rollback transaction
            self.adapter.conn.rollback()
            raise QueryError(
                f"Failed to update repository: {e}",
                details={
                    "repo_id": repo_id,
                    "error": str(e)
                }
            )

    def remove_repository(self, repo_id: str, delete_nodes: bool = False) -> bool:
        """Remove a repository from the knowledge graph.

        Args:
            repo_id: The ID of the repository to remove.
            delete_nodes: Whether to delete all nodes from this repository.
                If False, nodes will remain but won't be associated with any repository.

        Returns:
            True if the repository was removed, False otherwise.

        Raises:
            QueryError: If the repository doesn't exist or cannot be removed.
        """
        if not self.adapter.is_connected():
            raise DatabaseError("Not connected to database")

        # Check if repository exists
        repos = self.list_repositories()
        repo_exists = any(repo["id"] == repo_id for repo in repos)

        if not repo_exists:
            raise QueryError(f"Repository with ID '{repo_id}' does not exist")

        try:
            # Start a transaction
            self.adapter.conn.execute("BEGIN TRANSACTION")

            # Remove from active repositories
            if repo_id in self.active_repos:
                self.active_repos.remove(repo_id)

            # Remove from repositories table
            self.adapter.conn.execute(
                "DELETE FROM repositories WHERE id = ?",
                (repo_id,)
            )

            if delete_nodes:
                # Delete all nodes from this repository
                self.adapter.conn.execute(
                    "DELETE FROM nodes WHERE repo_id = ?",
                    (repo_id,)
                )

                # Find and delete orphaned edges
                # This is a bit complex as we need to find edges where either src or dst
                # was in the deleted repository and has been deleted
                self.adapter.conn.execute("""
                    DELETE FROM edges
                    WHERE src IN (
                        SELECT id FROM nodes WHERE repo_id = ?
                    ) OR dst IN (
                        SELECT id FROM nodes WHERE repo_id = ?
                    )
                """, (repo_id, repo_id))
            else:
                # Update nodes to remove repo_id
                self.adapter.conn.execute(
                    "UPDATE nodes SET repo_id = NULL WHERE repo_id = ?",
                    (repo_id,)
                )

            # Commit transaction
            self.adapter.conn.commit()
            return True

        except Exception as e:
            # Rollback transaction
            self.adapter.conn.rollback()
            raise QueryError(
                f"Failed to remove repository: {e}",
                details={
                    "repo_id": repo_id,
                    "error": str(e)
                }
            )

    def get_active_repositories(self) -> List[Dict[str, Any]]:
        """Get the active repositories.

        Returns:
            List of active repository dictionaries.

        Raises:
            QueryError: If getting active repositories fails.
        """
        try:
            if not self.active_repos:
                # If no active repositories, ensure current repository
                self.ensure_repository()

            # Get repository details for active repositories
            repos = []
            for repo_id in self.active_repos:
                cursor = self.adapter.conn.execute(
                    "SELECT * FROM repositories WHERE id = ?",
                    (repo_id,)
                )
                row = cursor.fetchone()
                if row:
                    repo = dict(row)

                    # Parse metadata if it exists
                    if repo.get("metadata"):
                        import json
                        repo["metadata"] = json.loads(repo["metadata"])

                    repos.append(repo)

            return repos
        except Exception as e:
            raise QueryError(f"Failed to get active repositories: {e}") from e

    def get_node_by_id(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get a node by its ID.

        Args:
            node_id: The ID of the node.

        Returns:
            The node as a dictionary, or None if it doesn't exist.

        Raises:
            QueryError: If getting the node fails.
        """
        try:
            return self.adapter.get_node_by_id(node_id)
        except Exception as e:
            raise QueryError(f"Failed to get node by ID: {e}") from e

    def add_nodes_and_edges(self, nodes: List[Node], edges: List[Edge]) -> None:
        """Add nodes and edges to the knowledge graph.

        Args:
            nodes: The nodes to add.
            edges: The edges to add.

        Raises:
            BuildError: If adding nodes and edges fails.
        """
        try:
            self.adapter.add_nodes_and_edges(nodes, edges)
        except Exception as e:
            raise BuildError(f"Failed to add nodes and edges: {e}") from e

    def get_node_count(self) -> int:
        """Get the number of nodes in the knowledge graph.

        Returns:
            The number of nodes.

        Raises:
            QueryError: If getting the node count fails.
        """
        try:
            return self.adapter.get_node_count()
        except Exception as e:
            raise QueryError(f"Failed to get node count: {e}") from e

    def get_edge_count(self) -> int:
        """Get the number of edges in the knowledge graph.

        Returns:
            The number of edges.

        Raises:
            QueryError: If getting the edge count fails.
        """
        try:
            return self.adapter.get_edge_count()
        except Exception as e:
            raise QueryError(f"Failed to get edge count: {e}") from e

    def get_edges_by_src(self, src_id: str) -> List[Dict[str, Any]]:
        """Get edges by source node ID.

        Args:
            src_id: The ID of the source node.

        Returns:
            A list of edges as dictionaries.

        Raises:
            QueryError: If getting the edges fails.
        """
        try:
            return self.adapter.get_edges_by_src(src_id)
        except Exception as e:
            raise QueryError(f"Failed to get edges by source: {e}") from e

    def get_edges_by_dst(self, dst_id: str) -> List[Dict[str, Any]]:
        """Get edges by destination node ID.

        Args:
            dst_id: The ID of the destination node.

        Returns:
            A list of edges as dictionaries.

        Raises:
            QueryError: If getting the edges fails.
        """
        try:
            return self.adapter.get_edges_by_dst(dst_id)
        except Exception as e:
            raise QueryError(f"Failed to get edges by destination: {e}") from e

    def close(self) -> None:
        """Close the connection to the database.

        Raises:
            AdapterError: If closing the connection fails.
        """
        try:
            if self.adapter and self.adapter.is_connected():
                self.adapter.disconnect()
        except Exception as e:
            raise AdapterError(f"Failed to close database connection: {e}") from e

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        self.close()

    # Build API methods

    def build(
        self,
        repo_path=None,
        include_github=True,
        include_linear=False,
        include_architecture=True,
        use_llm=True,
        llm_provider="openai",
        llm_model="gpt-4.1",
        llm_enhancement_level="standard",
        verbose=False,
    ):
        """Build or refresh the knowledge graph for the current repository.

        This method builds or refreshes the knowledge graph from various sources,
        including Git, GitHub, Linear, and ADRs. It can also enhance the graph with
        LLM-derived insights.

        Args:
            repo_path: Path to the Git repository. If None, uses the repo_path from initialization.
            include_github: Whether to include GitHub data in the graph.
            include_linear: Whether to include Linear data in the graph.
            include_architecture: Whether to extract architecture components. Default is True.
            use_llm: Whether to use an LLM to enhance the graph. Default is True.
            llm_provider: The LLM provider to use. Default is "openai".
            llm_model: The LLM model to use. Default is "gpt-4.1".
            llm_enhancement_level: The level of LLM enhancement to apply ("minimal", "standard", or "deep").
            verbose: Whether to print verbose output during the build process.

        Returns:
            A dictionary containing information about the build process, including
            the number of nodes and edges added, updated, and removed.

        Raises:
            BuildError: If building the knowledge graph fails.
        """
        # Use the repo_path from initialization if not provided
        if repo_path is None:
            repo_path = self.repo_path

        # Import here to avoid circular imports
        from arc_memory.auto_refresh.core import refresh_knowledge_graph

        try:
            # Ensure repository exists and get its ID
            repo_id = self.ensure_repository()

            result = refresh_knowledge_graph(
                repo_path=repo_path,
                include_github=include_github,
                include_linear=include_linear,
                include_architecture=include_architecture,
                use_llm=use_llm,
                llm_provider=llm_provider,
                llm_model=llm_model,
                llm_enhancement_level=llm_enhancement_level,
                verbose=verbose,
                repo_id=repo_id  # Pass repository ID to ensure nodes are properly tagged
            )

            # Make sure this repository is in the active repositories list
            if repo_id not in self.active_repos:
                self.active_repos.append(repo_id)

            return result
        except Exception as e:
            error_str = str(e)

            # Provide more specific error messages based on the type of exception
            if "Permission denied" in error_str:
                raise BuildError(
                    what_happened="Failed to build knowledge graph due to permission issues",
                    why_it_happened=f"The process doesn't have permission to access required files: {error_str}",
                    how_to_fix_it="Check file permissions for the repository directory and ensure you have read/write access. "
                                 "If using Git operations, ensure you have proper Git credentials configured.",
                    details={"error": error_str, "repo_path": str(repo_path)}
                ) from e
            elif "No such file or directory" in error_str:
                raise BuildError(
                    what_happened="Failed to build knowledge graph due to missing files",
                    why_it_happened=f"Required files or directories could not be found: {error_str}",
                    how_to_fix_it="Verify that the repository path exists and contains a valid Git repository. "
                                 "If you specified a custom path, check that it's correct.",
                    details={"error": error_str, "repo_path": str(repo_path)}
                ) from e
            elif "API rate limit exceeded" in error_str or "rate limit" in error_str.lower():
                raise BuildError(
                    what_happened="Failed to build knowledge graph due to API rate limits",
                    why_it_happened=f"GitHub API rate limit exceeded: {error_str}",
                    how_to_fix_it="Wait for the rate limit to reset (usually 1 hour) or use a GitHub token with higher rate limits. "
                                 "You can set the GITHUB_TOKEN environment variable or use the --github-token option.",
                    details={"error": error_str, "repo_path": str(repo_path)}
                ) from e
            elif "LLM" in error_str or "model" in error_str.lower() or "openai" in error_str.lower() or "ollama" in error_str.lower():
                raise BuildError(
                    what_happened="Failed to build knowledge graph due to LLM-related issues",
                    why_it_happened=f"Error with LLM processing: {error_str}",
                    how_to_fix_it="Check your LLM configuration. For OpenAI, ensure OPENAI_API_KEY is set correctly. "
                                 "For Ollama, ensure it's installed and running. You can also try with use_llm=False "
                                 "to build without LLM enhancement.",
                    details={"error": error_str, "repo_path": str(repo_path), "llm_provider": llm_provider, "llm_model": llm_model}
                ) from e
            else:
                raise BuildError(
                    what_happened="Failed to build knowledge graph",
                    why_it_happened=f"Error during knowledge graph build: {error_str}",
                    how_to_fix_it="Check the error message for details. Ensure you have the necessary permissions and dependencies. "
                                 "You can also try running with verbose=True for more detailed logs.",
                    details={"error": error_str, "repo_path": str(repo_path)}
                ) from e

    def build_repository(
        self,
        repo_id: str,
        include_github=True,
        include_linear=False,
        include_architecture=True,
        use_llm=True,
        llm_provider="openai",
        llm_model="gpt-4.1",
        llm_enhancement_level="standard",
        verbose=False,
    ):
        """Build or refresh the knowledge graph for a specific repository.

        Args:
            repo_id: Repository ID to build.
            include_github: Whether to include GitHub data in the graph.
            include_linear: Whether to include Linear data in the graph.
            include_architecture: Whether to extract architecture components.
            use_llm: Whether to use an LLM to enhance the graph.
            llm_provider: The LLM provider to use.
            llm_model: The LLM model to use.
            llm_enhancement_level: The level of LLM enhancement to apply.
            verbose: Whether to print verbose output during the build process.

        Returns:
            A dictionary containing information about the build process.

        Raises:
            BuildError: If building the knowledge graph fails.
        """
        try:
            # Get repository information
            cursor = self.adapter.conn.execute(
                "SELECT * FROM repositories WHERE id = ?",
                (repo_id,)
            )
            repo = cursor.fetchone()

            if not repo:
                raise BuildError(
                    what_happened=f"Repository with ID {repo_id} not found",
                    why_it_happened="The specified repository ID does not exist in the database",
                    how_to_fix_it="Check the repository ID or use list_repositories() to see available repositories",
                    details={"repo_id": repo_id}
                )

            # Get repository path
            repo_path = Path(repo["local_path"])

            # Import here to avoid circular imports
            from arc_memory.auto_refresh.core import refresh_knowledge_graph

            # Build the knowledge graph for this repository
            result = refresh_knowledge_graph(
                repo_path=repo_path,
                include_github=include_github,
                include_linear=include_linear,
                include_architecture=include_architecture,
                use_llm=use_llm,
                llm_provider=llm_provider,
                llm_model=llm_model,
                llm_enhancement_level=llm_enhancement_level,
                verbose=verbose,
                repo_id=repo_id  # Pass repository ID to ensure nodes are properly tagged
            )

            # Make sure this repository is in the active repositories list
            if repo_id not in self.active_repos:
                self.active_repos.append(repo_id)

            return result
        except Exception as e:
            error_str = str(e)

            # Provide more specific error messages based on the type of exception
            if "Permission denied" in error_str:
                raise BuildError(
                    what_happened=f"Failed to build knowledge graph for repository {repo_id} due to permission issues",
                    why_it_happened=f"The process doesn't have permission to access required files: {error_str}",
                    how_to_fix_it="Check file permissions for the repository directory and ensure you have read/write access. "
                                 "If using Git operations, ensure you have proper Git credentials configured.",
                    details={"error": error_str, "repo_id": repo_id, "repo_path": str(repo_path) if 'repo_path' in locals() else None}
                ) from e
            elif "No such file or directory" in error_str:
                raise BuildError(
                    what_happened=f"Failed to build knowledge graph for repository {repo_id} due to missing files",
                    why_it_happened=f"Required files or directories could not be found: {error_str}",
                    how_to_fix_it="Verify that the repository path exists and contains a valid Git repository. "
                                 "Use list_repositories() to check the registered path for this repository.",
                    details={"error": error_str, "repo_id": repo_id, "repo_path": str(repo_path) if 'repo_path' in locals() else None}
                ) from e
            elif "API rate limit exceeded" in error_str or "rate limit" in error_str.lower():
                raise BuildError(
                    what_happened=f"Failed to build knowledge graph for repository {repo_id} due to API rate limits",
                    why_it_happened=f"GitHub API rate limit exceeded: {error_str}",
                    how_to_fix_it="Wait for the rate limit to reset (usually 1 hour) or use a GitHub token with higher rate limits. "
                                 "You can set the GITHUB_TOKEN environment variable or use the --github-token option.",
                    details={"error": error_str, "repo_id": repo_id}
                ) from e
            elif "LLM" in error_str or "model" in error_str.lower() or "openai" in error_str.lower() or "ollama" in error_str.lower():
                raise BuildError(
                    what_happened=f"Failed to build knowledge graph for repository {repo_id} due to LLM-related issues",
                    why_it_happened=f"Error with LLM processing: {error_str}",
                    how_to_fix_it="Check your LLM configuration. For OpenAI, ensure OPENAI_API_KEY is set correctly. "
                                 "For Ollama, ensure it's installed and running. You can also try with use_llm=False "
                                 "to build without LLM enhancement.",
                    details={"error": error_str, "repo_id": repo_id, "llm_provider": llm_provider, "llm_model": llm_model}
                ) from e
            else:
                raise BuildError(
                    what_happened=f"Failed to build knowledge graph for repository {repo_id}",
                    why_it_happened=f"Error during knowledge graph build: {error_str}",
                    how_to_fix_it="Check the error message for details. Ensure you have the necessary permissions and dependencies. "
                                 "You can also try running with verbose=True for more detailed logs.",
                    details={"error": error_str, "repo_id": repo_id}
                ) from e

    # Query API methods

    def query(
        self,
        question: str,
        max_results: int = 5,
        max_hops: int = 3,
        include_causal: bool = True,
        cache: bool = True,
        callback: Optional[ProgressCallback] = None,
        timeout: int = 60,
        repo_ids: Optional[List[str]] = None
    ) -> QueryResult:
        """Query the knowledge graph using natural language.

        This method enables natural language queries about the codebase, focusing on
        causal relationships and decision trails. It's particularly useful for understanding
        why certain changes were made and their implications.

        Args:
            question: The natural language question to ask.
            max_results: Maximum number of results to return.
            max_hops: Maximum number of hops in the graph traversal.
            include_causal: Whether to prioritize causal relationships.
            cache: Whether to use cached results if available. When True (default),
                results are cached and retrieved from cache if a matching query exists.
                Set to False to force a fresh query execution.
            callback: Optional callback for progress reporting.
            timeout: Maximum time in seconds to wait for Ollama response.
            repo_ids: Optional list of repository IDs to filter by. If None, uses active repositories.

        Returns:
            A QueryResult containing the answer and supporting evidence.

        Raises:
            QueryError: If the query fails.

        Note:
            This method requires Ollama to be installed and running. If Ollama is not
            available, it will return an error message with installation instructions.
            Install Ollama from https://ollama.ai/download and start it with 'ollama serve'.
        """
        from arc_memory.sdk.query import query_knowledge_graph

        # If no repo_ids provided, use active repositories
        if repo_ids is None:
            # If no active repositories, ensure current repository
            if not self.active_repos:
                self.ensure_repository()
            repo_ids = self.active_repos

        return query_knowledge_graph(
            adapter=self.adapter,
            question=question,
            max_results=max_results,
            max_hops=max_hops,
            include_causal=include_causal,
            cache=cache,
            callback=callback,
            timeout=timeout,
            repo_ids=repo_ids
        )

    # Decision Trail API methods

    def get_decision_trail(
        self,
        file_path: str,
        line_number: int,
        max_results: int = 5,
        max_hops: int = 3,
        include_rationale: bool = True,
        cache: bool = True,
        callback: Optional[ProgressCallback] = None
    ) -> List[DecisionTrailEntry]:
        """Get the decision trail for a specific line in a file.

        This method traces the history of a specific line in a file, showing the commit
        that last modified it and related entities such as PRs, issues, and ADRs. It's
        particularly useful for understanding why a particular piece of code exists.

        Args:
            file_path: Path to the file, relative to the repository root.
            line_number: Line number to trace (1-based).
            max_results: Maximum number of results to return.
            max_hops: Maximum number of hops in the graph traversal.
            include_rationale: Whether to extract decision rationales.
            cache: Whether to use cached results if available. When True (default),
                results are cached and retrieved from cache if a matching query exists.
                Set to False to force a fresh query execution.
            callback: Optional callback for progress reporting.

        Returns:
            A list of DecisionTrailEntry objects representing the decision trail.

        Raises:
            QueryError: If getting the decision trail fails.
        """
        from arc_memory.sdk.decision_trail import get_decision_trail
        return get_decision_trail(
            adapter=self.adapter,
            file_path=file_path,
            line_number=line_number,
            max_results=max_results,
            max_hops=max_hops,
            include_rationale=include_rationale,
            cache=cache,
            callback=callback
        )

    # Entity Relationship API methods

    def get_related_entities(
        self,
        entity_id: str,
        relationship_types: Optional[List[str]] = None,
        direction: str = "both",
        max_results: int = 10,
        include_properties: bool = True,
        cache: bool = True,
        callback: Optional[ProgressCallback] = None
    ) -> List[RelatedEntity]:
        """Get entities related to a specific entity.

        This method retrieves entities that are directly connected to the specified entity
        in the knowledge graph. It supports filtering by relationship type and direction.

        Args:
            entity_id: The ID of the entity.
            relationship_types: Optional list of relationship types to filter by.
            direction: Direction of relationships to include ("outgoing", "incoming", or "both").
            max_results: Maximum number of results to return.
            include_properties: Whether to include edge properties in the results.
            cache: Whether to use cached results if available. When True (default),
                results are cached and retrieved from cache if a matching query exists.
                Set to False to force a fresh query execution.
            callback: Optional callback for progress reporting.

        Returns:
            A list of RelatedEntity objects.

        Raises:
            QueryError: If getting related entities fails.
        """
        from arc_memory.sdk.relationships import get_related_entities
        return get_related_entities(
            adapter=self.adapter,
            entity_id=entity_id,
            relationship_types=relationship_types,
            direction=direction,
            max_results=max_results,
            include_properties=include_properties,
            cache=cache,
            callback=callback
        )

    def get_entity_details(
        self,
        entity_id: str,
        include_related: bool = True,
        cache: bool = True,
        callback: Optional[ProgressCallback] = None
    ) -> EntityDetails:
        """Get detailed information about an entity.

        This method retrieves detailed information about an entity, including its
        properties and optionally its relationships with other entities.

        Args:
            entity_id: The ID of the entity.
            include_related: Whether to include related entities.
            cache: Whether to use cached results if available. When True (default),
                results are cached and retrieved from cache if a matching query exists.
                Set to False to force a fresh query execution.
            callback: Optional callback for progress reporting.

        Returns:
            An EntityDetails object.

        Raises:
            QueryError: If getting entity details fails.
        """
        from arc_memory.sdk.relationships import get_entity_details
        return get_entity_details(
            adapter=self.adapter,
            entity_id=entity_id,
            include_related=include_related,
            cache=cache,
            callback=callback
        )

    # Architecture API methods

    def get_architecture_components(
        self,
        component_type: Optional[str] = None,
        parent_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get architecture components from the knowledge graph.

        Args:
            component_type: Filter by component type (system, service, component, interface)
            parent_id: Filter by parent component ID

        Returns:
            List of architecture components

        Raises:
            QueryError: If getting architecture components fails.
        """
        try:
            # Ensure repository exists
            repo_id = self.ensure_repository()

            # Build query based on parameters
            query = "SELECT * FROM nodes WHERE "
            params = []
            conditions = []

            # Filter by repository
            conditions.append("repo_id = ?")
            params.append(repo_id)

            # Filter by component type
            if component_type:
                conditions.append("type = ?")
                params.append(component_type)
            else:
                conditions.append("type IN ('system', 'service', 'component', 'interface')")

            # Combine conditions
            query += " AND ".join(conditions)

            # Execute query
            cursor = self.adapter.conn.execute(query, tuple(params))
            components = [dict(row) for row in cursor.fetchall()]

            # Filter by parent if needed
            if parent_id:
                # Get all edges where parent_id is the source
                cursor = self.adapter.conn.execute(
                    "SELECT * FROM edges WHERE src = ? AND rel = 'CONTAINS'",
                    (parent_id,)
                )
                # Get IDs of children
                child_ids = [row["dst"] for row in cursor.fetchall()]
                # Filter components by child IDs
                components = [c for c in components if c["id"] in child_ids]

            # Parse extra field
            for component in components:
                if component.get("extra"):
                    import json
                    component["extra"] = json.loads(component["extra"])

            return components
        except Exception as e:
            raise QueryError(f"Failed to get architecture components: {e}") from e

    # Component Impact API methods

    def analyze_component_impact(
        self,
        component_id: str,
        impact_types: Optional[List[str]] = None,
        max_depth: int = 3,
        cache: bool = True,
        callback: Optional[ProgressCallback] = None
    ) -> List[ImpactResult]:
        """Analyze the potential impact of changes to a component.

        This method identifies components that may be affected by changes to the
        specified component, based on historical co-change patterns and explicit
        dependencies in the knowledge graph. It helps predict the "blast radius"
        of changes, which is useful for planning refactoring efforts, assessing risk,
        and understanding the architecture of your codebase.

        Args:
            component_id: The ID of the component to analyze. This can be a file, directory,
                module, or any other component in your codebase. Format should be
                "type:identifier", e.g., "file:src/auth/login.py".
            impact_types: Types of impact to include in the analysis. Options are:
                - "direct": Components that directly depend on or are depended upon by the target
                - "indirect": Components connected through a chain of dependencies
                - "potential": Components that historically changed together with the target
                If None, all impact types will be included.
            max_depth: Maximum depth of indirect dependency analysis. Higher values will
                analyze more distant dependencies but may take longer. Values between
                2-5 are recommended for most codebases.
            cache: Whether to use cached results if available. When True (default),
                results are cached and retrieved from cache if a matching query exists.
                Set to False to force a fresh query execution.
            callback: Optional callback for progress reporting. If provided,
                it will be called at various stages of the analysis with progress updates.

        Returns:
            A list of ImpactResult objects representing affected components. Each result
            includes the component ID, type, title, impact type, impact score (0-1),
            and the path of dependencies from the target component.

        Raises:
            QueryError: If the impact analysis fails due to database errors, invalid
                component ID, or other issues. The error message will include details
                about what went wrong and how to fix it.

        Example:
            ```python
            # Initialize Arc
            arc = Arc(repo_path="./")

            # Analyze impact on a file
            results = arc.analyze_component_impact(
                component_id="file:src/auth/login.py",
                impact_types=["direct", "indirect"],
                max_depth=3
            )

            # Process results
            for result in results:
                print(f"{result.title}: {result.impact_score} ({result.impact_type})")

            # Find high-impact components
            high_impact = [r for r in results if r.impact_score > 0.7]
            ```
        """
        from arc_memory.sdk.impact import analyze_component_impact
        return analyze_component_impact(
            adapter=self.adapter,
            component_id=component_id,
            impact_types=impact_types,
            max_depth=max_depth,
            cache=cache,
            callback=callback
        )

    # Temporal Analysis API methods

    def get_entity_history(
        self,
        entity_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        include_related: bool = False,
        cache: bool = True,
        callback: Optional[ProgressCallback] = None
    ) -> List[HistoryEntry]:
        """Get the history of an entity over time.

        This method retrieves the history of an entity, showing how it has changed
        over time and how it has been referenced by other entities.

        Args:
            entity_id: The ID of the entity.
            start_date: Optional start date for the history.
            end_date: Optional end date for the history.
            include_related: Whether to include related entities in the history.
            cache: Whether to use cached results if available. When True (default),
                results are cached and retrieved from cache if a matching query exists.
                Set to False to force a fresh query execution.
            callback: Optional callback for progress reporting.

        Returns:
            A list of HistoryEntry objects representing the entity's history.

        Raises:
            QueryError: If getting the entity history fails.
        """
        from arc_memory.sdk.temporal import get_entity_history
        return get_entity_history(
            adapter=self.adapter,
            entity_id=entity_id,
            start_date=start_date,
            end_date=end_date,
            include_related=include_related,
            cache=cache,
            callback=callback
        )

    # Framework Adapter API methods

    def get_adapter(self, framework: str) -> FrameworkAdapter:
        """Get a framework adapter by name.

        This method retrieves a framework adapter by name, which can be used to
        adapt Arc Memory functions to a specific agent framework.

        Args:
            framework: The name of the framework adapter to get.

        Returns:
            A framework adapter instance.

        Raises:
            FrameworkError: If the adapter cannot be found or initialized.
        """
        try:
            return get_adapter(framework)
        except Exception as e:
            raise FrameworkError(f"Failed to get framework adapter: {e}") from e

    def get_tools(self, framework: str) -> Any:
        """Get Arc Memory functions as tools for a specific framework.

        This method converts Arc Memory functions to tools that can be used
        with a specific agent framework.

        Args:
            framework: The name of the framework to adapt to.

        Returns:
            Framework-specific tools that can be used with the framework.

        Raises:
            FrameworkError: If the adapter cannot be found or initialized.
        """
        adapter = self.get_adapter(framework)

        # Get the functions to adapt
        functions = [
            self.query,
            self.get_decision_trail,
            self.get_related_entities,
            self.get_entity_details,
            self.analyze_component_impact,
            self.get_entity_history
        ]

        # Adapt the functions to the framework
        return adapter.adapt_functions(functions)

    def create_agent(self, framework: str, **kwargs) -> Any:
        """Create an agent using a specific framework.

        This method creates an agent using a specific framework, with
        Arc Memory functions available as tools.

        Args:
            framework: The name of the framework to use.
            **kwargs: Framework-specific parameters for creating an agent.

        Returns:
            A framework-specific agent instance.

        Raises:
            FrameworkError: If the adapter cannot be found or initialized.
        """
        adapter = self.get_adapter(framework)

        # Create the agent
        return adapter.create_agent(**kwargs)

    # Export API methods

    def export_graph(
        self,
        pr_sha: str,
        output_path: Union[str, Path],
        compress: bool = True,
        sign: bool = False,
        key_id: Optional[str] = None,
        base_branch: str = "main",
        max_hops: int = 3,
        optimize_for_llm: bool = True,
        include_causal: bool = True,
        callback: Optional[ProgressCallback] = None
    ) -> "ExportResult":
        """Export a relevant slice of the knowledge graph for a PR.

        This method exports a subset of the knowledge graph focused on the files
        modified in a specific PR, along with related nodes and edges. The export
        is saved as a JSON file that can be used by the GitHub App for PR reviews.

        Args:
            pr_sha: SHA of the PR head commit.
            output_path: Path to save the export file.
            compress: Whether to compress the output file.
            sign: Whether to sign the output file with GPG.
            key_id: GPG key ID to use for signing.
            base_branch: Base branch to compare against.
            max_hops: Maximum number of hops to traverse in the graph.
            optimize_for_llm: Whether to optimize the export data for LLM reasoning.
            include_causal: Whether to include causal relationships in the export.
            callback: Optional callback for progress reporting. If provided, this function
                will be called at various stages of the export process with progress updates.
                The callback receives three parameters: the current stage (a ProgressStage enum),
                a message describing the current operation, and a progress value between 0 and 1.

        Returns:
            ExportResult containing information about the exported file.

        Raises:
            QueryError: If exporting the graph fails.
        """
        try:
            from arc_memory.sdk.export import export_knowledge_graph

            # Convert output_path to Path
            output_path = Path(output_path)

            # Export the graph
            return export_knowledge_graph(
                adapter=self.adapter,
                repo_path=self.repo_path,
                pr_sha=pr_sha,
                output_path=output_path,
                compress=compress,
                sign=sign,
                key_id=key_id,
                base_branch=base_branch,
                max_hops=max_hops,
                optimize_for_llm=optimize_for_llm,
                include_causal=include_causal,
                callback=callback
            )
        except Exception as e:
            raise QueryError(f"Failed to export graph: {e}") from e
