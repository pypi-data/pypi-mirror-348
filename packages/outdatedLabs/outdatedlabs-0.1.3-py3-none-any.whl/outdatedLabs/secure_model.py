"""
Secure Model Training Module
"""
import os
import time
import logging
import requests
import joblib
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from tqdm import tqdm
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SecureModel:
    """Secure Model Training Class"""
    
    def __init__(self, server_url: str = "http://localhost:3000"):
        """
        Initialize the SecureModel.
        
        Args:
            server_url (str): URL of the ML training server
        """
        self.server_url = server_url.rstrip('/')
        self.job_id = None
        self.model = None
        self.metrics = None
        
        # Test server connection
        try:
            response = requests.get(f"{self.server_url}/health")
            response.raise_for_status()
            logger.info(f"Successfully connected to server at {self.server_url}")
        except requests.exceptions.ConnectionError:
            logger.error(f"Could not connect to server at {self.server_url}. Please ensure the server is running.")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to server: {str(e)}")
            raise
        
    def set_server_url(self, server_url: str) -> 'SecureModel':
        """
        Set the training server URL.
        
        Args:
            server_url (str): New URL for the ML training server
            
        Returns:
            SecureModel: Self for method chaining
        """
        self.server_url = server_url.rstrip('/')
        logger.info(f"Server URL set to: {self.server_url}")
        
        # Test new server connection
        try:
            response = requests.get(f"{self.server_url}/health")
            response.raise_for_status()
            logger.info(f"Successfully connected to new server at {self.server_url}")
        except requests.exceptions.ConnectionError:
            logger.error(f"Could not connect to server at {self.server_url}. Please ensure the server is running.")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to server: {str(e)}")
            raise
            
        return self
        
    @classmethod
    def linearRegression(cls, server_url: str = "http://localhost:3000") -> 'SecureModel':
        """
        Create a Linear Regression model.
        
        Args:
            server_url (str): URL of the ML training server
            
        Returns:
            SecureModel: A new SecureModel instance configured for linear regression
        """
        instance = cls(server_url)
        instance.algorithm = "linear_regression"
        return instance
    
    def fit(self, 
            dataset_hash: str,
            features: Optional[List[str]] = None,
            target: Optional[str] = None,
            params: Optional[Dict[str, Any]] = None) -> 'SecureModel':
        """
        Train the model using the specified dataset.
        
        Args:
            dataset_hash (str): The dataset hash in format "walrus://dataset_hash"
            features (List[str], optional): List of feature column names
            target (str, optional): Target column name
            params (Dict[str, Any], optional): Model parameters
            
        Returns:
            SecureModel: Self for method chaining
        """
        try:
            # Extract hash from walrus:// format
            if dataset_hash.startswith("walrus://"):
                dataset_hash = dataset_hash[9:]
            
            # Prepare training request
            request_data = {
                "dataset_hash": dataset_hash,
                "algorithm": self.algorithm,
                "params": params or {},
                "features": features,
                "target": target
            }
            
            logger.info(f"Starting training with parameters: {request_data}")
            
            # Start training job
            response = requests.post(
                f"{self.server_url}/train",
                json=request_data
            )
            response.raise_for_status()
            
            # Get job ID
            self.job_id = response.json()["job_id"]
            logger.info(f"Training job started with ID: {self.job_id}")
            
            # Wait for training to complete
            self._wait_for_completion()
            
            # Download and load the model
            self._download_model()
            
            return self
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            raise
    
    def _wait_for_completion(self, check_interval: int = 2) -> None:
        """Wait for the training job to complete."""
        with tqdm(desc="Training", unit="s") as pbar:
            while True:
                try:
                    response = requests.get(f"{self.server_url}/train/{self.job_id}/status")
                    response.raise_for_status()
                    status = response.json()
                    
                    # Convert status to uppercase for case-insensitive comparison
                    current_status = status["status"].upper()
                    
                    if current_status == "COMPLETE":
                        logger.info("Training completed successfully")
                        self.metrics = requests.get(f"{self.server_url}/train/{self.job_id}/metrics").json()
                        pbar.close()
                        return
                    elif current_status == "FAILED":
                        error = status.get("error", "Unknown error")
                        pbar.close()
                        raise Exception(f"Training failed: {error}")
                    
                    time.sleep(check_interval)
                    pbar.update(check_interval)
                except Exception as e:
                    pbar.close()
                    raise Exception(f"Error checking training status: {str(e)}")
    
    def _download_model(self) -> None:
        """Download the trained model."""
        try:
            response = requests.get(
                f"{self.server_url}/train/{self.job_id}/model",
                stream=True
            )
            response.raise_for_status()
            
            # Save model to temporary file
            temp_path = Path(f"model_{self.job_id}.joblib")
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Load the model
            self.model = joblib.load(temp_path)
            
            # Clean up
            temp_path.unlink()
            
            logger.info("Model downloaded and loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to download model: {str(e)}")
            raise
    
    def predict(self, X: Union[pd.DataFrame, List[List[float]]]) -> List[float]:
        """
        Make predictions using the trained model.
        
        Args:
            X: Input features as DataFrame or list of lists
            
        Returns:
            List[float]: Predicted values
        """
        if self.model is None:
            raise Exception("Model not trained. Call fit() first.")
        
        if isinstance(X, list):
            X = pd.DataFrame(X)
        
        return self.model.predict(X).tolist()
    
    def score(self, X: Union[pd.DataFrame, List[List[float]]], y: List[float]) -> Dict[str, float]:
        """
        Calculate model performance metrics.
        
        Args:
            X: Input features as DataFrame or list of lists
            y: True target values
            
        Returns:
            Dict[str, float]: Dictionary of metrics
        """
        if self.model is None:
            raise Exception("Model not trained. Call fit() first.")
        
        if isinstance(X, list):
            X = pd.DataFrame(X)
        
        y_pred = self.model.predict(X)
        return {
            "mse": mean_squared_error(y, y_pred),
            "r2": r2_score(y, y_pred)
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get training metrics.
        
        Returns:
            Dict[str, Any]: Training metrics
        """
        if self.metrics is None:
            raise Exception("Model not trained. Call fit() first.")
        return self.metrics 