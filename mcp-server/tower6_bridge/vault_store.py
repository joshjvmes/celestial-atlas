"""
Tower 6 Vault - Sacred Scroll Storage System

Stores and retrieves markdown scrolls with metadata.
Stored. Retrievable. Kind.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional


class VaultStore:
    """Storage system for Tower 6 sacred scrolls"""

    def __init__(self, root: Path, max_scroll_kb: int = 256):
        """
        Initialize Vault storage.

        Args:
            root: Root directory for vault storage
            max_scroll_kb: Maximum scroll size in KB
        """
        self.root = Path(root)
        self.max_scroll_kb = max_scroll_kb
        self.scroll_dir = self.root / "scrolls"
        self.scroll_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.root / "index.json"

        # Create index if it doesn't exist
        if not self.index_path.exists():
            self._write_index({"scrolls": []})

    def _read_index(self) -> Dict[str, Any]:
        """Read the scroll index"""
        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def _write_index(self, index: Dict[str, Any]) -> None:
        """Write the scroll index"""
        self.index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")

    def write_scroll(
        self, title: str, body_md: str, tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Write a new scroll to the Vault.

        Args:
            title: Scroll title
            body_md: Markdown content
            tags: Optional list of tags

        Returns:
            Scroll metadata entry

        Raises:
            ValueError: If scroll exceeds size limit
        """
        tags = tags or []

        # Check size limit
        body_size_kb = len(body_md.encode("utf-8")) / 1024
        if body_size_kb > self.max_scroll_kb:
            raise ValueError(
                f"Scroll exceeds size limit: {body_size_kb:.1f}KB > {self.max_scroll_kb}KB"
            )

        # Generate unique scroll ID
        timestamp = int(time.time())
        hash_suffix = abs(hash(title)) % 99999
        scroll_id = f"{timestamp}-{hash_suffix:05d}"

        # Write scroll file
        scroll_path = self.scroll_dir / f"{scroll_id}.md"
        scroll_path.write_text(body_md, encoding="utf-8")

        # Update index
        index = self._read_index()
        entry = {
            "id": scroll_id,
            "title": title,
            "tags": tags,
            "path": str(scroll_path),
            "ts": timestamp,
            "size_kb": round(body_size_kb, 2),
        }
        index["scrolls"].append(entry)
        self._write_index(index)

        return entry

    def read_scroll(self, scroll_id: str) -> Dict[str, Any]:
        """
        Read a scroll by ID.

        Args:
            scroll_id: The scroll identifier

        Returns:
            Dictionary with id, body_md, and metadata

        Raises:
            FileNotFoundError: If scroll doesn't exist
        """
        scroll_path = self.scroll_dir / f"{scroll_id}.md"
        if not scroll_path.exists():
            raise FileNotFoundError(f"Scroll not found: {scroll_id}")

        body_md = scroll_path.read_text(encoding="utf-8")

        # Find metadata in index
        index = self._read_index()
        metadata = None
        for s in index["scrolls"]:
            if s["id"] == scroll_id:
                metadata = s
                break

        return {
            "id": scroll_id,
            "body_md": body_md,
            "metadata": metadata,
        }

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search scrolls by title or tags.

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of matching scroll metadata entries (most recent first)
        """
        index = self._read_index()
        query_lower = query.lower().strip()
        results = []

        # Search in reverse chronological order
        for scroll in reversed(index["scrolls"]):
            # Build searchable text from title and tags
            haystack = (
                scroll.get("title", "") + " " + " ".join(scroll.get("tags", []))
            ).lower()

            if query_lower in haystack:
                results.append(scroll)

            if len(results) >= limit:
                break

        return results

    def list_all(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List all scrolls in reverse chronological order.

        Args:
            limit: Optional maximum number of scrolls to return

        Returns:
            List of scroll metadata entries
        """
        index = self._read_index()
        scrolls = list(reversed(index["scrolls"]))
        if limit is not None:
            scrolls = scrolls[:limit]
        return scrolls

    def delete_scroll(self, scroll_id: str) -> None:
        """
        Delete a scroll by ID.

        Args:
            scroll_id: The scroll identifier

        Raises:
            FileNotFoundError: If scroll doesn't exist
        """
        scroll_path = self.scroll_dir / f"{scroll_id}.md"
        if not scroll_path.exists():
            raise FileNotFoundError(f"Scroll not found: {scroll_id}")

        # Delete file
        scroll_path.unlink()

        # Remove from index
        index = self._read_index()
        index["scrolls"] = [s for s in index["scrolls"] if s["id"] != scroll_id]
        self._write_index(index)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get Vault statistics.

        Returns:
            Dictionary with scroll count, total size, etc.
        """
        index = self._read_index()
        total_size_kb = sum(s.get("size_kb", 0) for s in index["scrolls"])

        return {
            "scroll_count": len(index["scrolls"]),
            "total_size_kb": round(total_size_kb, 2),
            "vault_path": str(self.root),
        }
