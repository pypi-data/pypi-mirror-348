from datetime import datetime
from typing import List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from ..config import MongoDBConfig
from ..models.project import Project


class MongoDBClient:
    def __init__(self):
        self.config = MongoDBConfig()
        self._client = None
        self._db = None
        self._collection = None
        self.connect()

    def connect(self):
        """Establish connection to MongoDB"""
        if self._client is None:
            self._client = MongoClient(self.config.uri)
            self._db = self._client[self.config.database]
            self._collection = self._db[self.config.collection]

    def close(self):
        """Close MongoDB connection"""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None
            self._collection = None

    @property
    def collection(self) -> Collection:
        if self._collection is None:
            self.connect()
        return self._collection
    
    def convert_logs_to_list(self, logs: str) -> List[str]:
        return [log.strip() for log in logs.split("\n") if log.strip()]

    def update_project_status(
        self,
        project_name: str,
        current_run_status: str,
        last_run_date: datetime,
        logs: str,
        last_run_command: str
    ) -> Project:
        """
        Updates or creates a project status in MongoDB.
        
        Args:
            project_name: Name of the project
            current_run_status: Current status of the run
            last_run_date: Timestamp of the last run
            logs: Optional list of log messages
            last_run_command: Optional command that was last run
            
        Returns:
            Project: Updated project instance
        """
        # Get the current state before updating
        current_doc = self.collection.find_one({"name": project_name})
        
        project = Project(
            name=project_name,
            current_run_status=current_run_status,
            last_run_date=last_run_date,
            logs=self.convert_logs_to_list(logs),
            last_run_command=last_run_command
        )
        
        update_dict = project.to_dict()
        
        if current_doc:
            # Create history entry from current state
            history_entry = {
                "run_status": current_doc.get("current_run_status", None),
                "run_date": current_doc.get("last_run_date", None),
                "logs": current_doc.get("logs", []),
                "run_command": current_doc.get("last_run_command", None)
            }
            
            self.collection.update_one(
                {"name": project_name},
                {
                    "$set": update_dict,
                    "$push": {
                        "history": {
                            "$each": [history_entry],
                            # "$slice": -100  # Keep only the last 100 entries
                        }
                    }
                }
            )
        else:
            raise ValueError(f"Project {project_name} not found")

        return project 