import pytest
from sovereign_control.core import SovereignControlProtocol
from sovereign_control.security import SecurityProtocol
from sovereign_control.quantum import QuantumStateManager

@pytest.fixture
def sovereign_protocol():
    return SovereignControlProtocol()

@pytest.fixture
def security_protocol():
    return SecurityProtocol()

@pytest.fixture
def quantum_manager():
    return QuantumStateManager()

def test_sovereign_initialization(sovereign_protocol):
    assert sovereign_protocol.is_active
    assert not sovereign_protocol.is_emergency_shutdown
    assert sovereign_protocol.security_level == "MAXIMUM"

def test_security_protocol(security_protocol):
    # Test biometric verification
    assert security_protocol.verify_biometrics("test_user") is False  # Should fail without real biometrics
    
    # Test emergency shutdown
    security_protocol.trigger_emergency_shutdown()
    assert security_protocol.is_emergency_shutdown

def test_quantum_state(quantum_manager):
    # Test quantum state initialization
    assert quantum_manager.get_state() == "STABLE"
    
    # Test state transition
    quantum_manager.transition_state("ACTIVE")
    assert quantum_manager.get_state() == "ACTIVE"

def test_protocol_integration(sovereign_protocol, security_protocol, quantum_manager):
    # Test full protocol integration
    sovereign_protocol.initialize()
    assert sovereign_protocol.is_active
    
    # Test emergency shutdown flow
    security_protocol.trigger_emergency_shutdown()
    sovereign_protocol.handle_emergency_shutdown()
    assert not sovereign_protocol.is_active
    assert quantum_manager.get_state() == "SHUTDOWN"

def test_protocol_recovery(sovereign_protocol, security_protocol, quantum_manager):
    # Test system recovery after shutdown
    security_protocol.trigger_emergency_shutdown()
    sovereign_protocol.handle_emergency_shutdown()
    
    # Attempt recovery
    sovereign_protocol.initialize()
    assert sovereign_protocol.is_active
    assert quantum_manager.get_state() == "STABLE" 