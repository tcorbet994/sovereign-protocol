from locust import HttpUser, task, between

class SovereignProtocolUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Initialize user session."""
        # Add authentication if needed
        pass
    
    @task(1)
    def access_interface(self):
        """Access the main interface."""
        self.client.get("/")
    
    @task(2)
    def stream_consciousness(self):
        """Stream consciousness data."""
        self.client.get("/stream/consciousness")
    
    @task(3)
    def monitor_quantum_state(self):
        """Monitor quantum state."""
        self.client.get("/monitor/quantum")
    
    @task(4)
    def verify_biometrics(self):
        """Verify biometric data."""
        self.client.post("/verify/biometric", json={
            "type": "test",
            "data": "test_data"
        })
    
    @task(5)
    def emergency_shutdown(self):
        """Test emergency shutdown endpoint."""
        self.client.post("/emergency/shutdown", json={
            "reason": "test",
            "timestamp": "2024-01-01T00:00:00Z"
        }) 