import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from sovereign_control.core import SovereignControlProtocol
from sovereign_control.security import SecurityProtocol
from sovereign_control.quantum import QuantumStateManager

@pytest.fixture
def protocol():
    security = SecurityProtocol()
    quantum = QuantumStateManager()
    return SovereignControlProtocol(security, quantum)

def test_concurrent_operations(protocol):
    """Benchmark concurrent operations performance."""
    def run_operation():
        protocol.security.verify_biometrics("test_user")
        protocol.quantum.transition_state("ACTIVE")
        protocol.stream_consciousness_data()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(run_operation) for _ in range(100)]
        start_time = time.time()
        for future in futures:
            future.result()
        end_time = time.time()
    
    total_time = end_time - start_time
    assert total_time < 5.0  # Should complete within 5 seconds

@pytest.mark.asyncio
async def test_async_operations(protocol):
    """Benchmark asynchronous operations performance."""
    async def run_async_operation():
        await protocol.stream_consciousness_data()
        await protocol.handle_websocket_message({"type": "test"})
    
    tasks = [run_async_operation() for _ in range(50)]
    start_time = time.time()
    await asyncio.gather(*tasks)
    end_time = time.time()
    
    total_time = end_time - start_time
    assert total_time < 3.0  # Should complete within 3 seconds

def test_memory_usage(protocol):
    """Benchmark memory usage under load."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Generate large dataset
    large_data = [{"type": "test", "data": "x" * 1000} for _ in range(1000)]
    
    # Process data
    for data in large_data:
        protocol.handle_websocket_message(data)
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    assert memory_increase < 100 * 1024 * 1024  # Less than 100MB increase

def test_cpu_usage(protocol):
    """Benchmark CPU usage under load."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_cpu = process.cpu_percent()
    
    # Perform CPU-intensive operations
    for _ in range(1000):
        protocol.security.encrypt_data("test_data" * 100)
    
    final_cpu = process.cpu_percent()
    cpu_increase = final_cpu - initial_cpu
    
    assert cpu_increase < 50  # Less than 50% CPU increase

def test_network_performance(protocol):
    """Benchmark network operations performance."""
    import requests
    import time
    
    def make_request():
        response = requests.get("http://localhost:8000/stream/consciousness")
        return response.status_code == 200
    
    start_time = time.time()
    results = [make_request() for _ in range(50)]
    end_time = time.time()
    
    total_time = end_time - start_time
    success_rate = sum(1 for r in results if r) / len(results)
    
    assert total_time < 10.0  # Should complete within 10 seconds
    assert success_rate > 0.95  # 95% success rate

def test_database_operations(protocol):
    """Benchmark database operations performance."""
    def db_operation():
        protocol.quantum.save_state("ACTIVE")
        protocol.quantum.get_state_history()
    
    start_time = time.time()
    for _ in range(100):
        db_operation()
    end_time = time.time()
    
    total_time = end_time - start_time
    assert total_time < 2.0  # Should complete within 2 seconds 