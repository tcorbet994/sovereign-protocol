import pytest
import time
from sovereign_control.core import SovereignControlProtocol
from sovereign_control.security import SecurityProtocol
from sovereign_control.quantum import QuantumStateManager

@pytest.fixture
def protocol():
    security = SecurityProtocol()
    quantum = QuantumStateManager()
    return SovereignControlProtocol(security, quantum)

def test_biometric_verification_speed(protocol):
    """Benchmark biometric verification performance."""
    def verify():
        protocol.security.verify_biometrics("test_user")
    
    result = pytest.benchmark(verify)
    assert result.stats.total < 0.1  # Should complete within 100ms

def test_quantum_state_transition(protocol):
    """Benchmark quantum state transition performance."""
    def transition():
        protocol.quantum.transition_state("ACTIVE")
    
    result = pytest.benchmark(transition)
    assert result.stats.total < 0.05  # Should complete within 50ms

def test_emergency_shutdown(protocol):
    """Benchmark emergency shutdown performance."""
    def shutdown():
        protocol.handle_emergency_shutdown()
    
    result = pytest.benchmark(shutdown)
    assert result.stats.total < 0.2  # Should complete within 200ms

def test_consciousness_streaming(protocol):
    """Benchmark consciousness streaming performance."""
    def stream():
        protocol.stream_consciousness_data()
    
    result = pytest.benchmark(stream)
    assert result.stats.total < 0.15  # Should complete within 150ms

def test_websocket_communication(protocol):
    """Benchmark WebSocket communication performance."""
    def communicate():
        protocol.handle_websocket_message({"type": "test"})
    
    result = pytest.benchmark(communicate)
    assert result.stats.total < 0.1  # Should complete within 100ms 