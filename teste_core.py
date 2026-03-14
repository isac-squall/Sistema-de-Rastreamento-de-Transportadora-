from core.services.container import ServiceContainer

try:
    container = ServiceContainer.create()
    print('Arquitetura modular funcionando!')
    print(f'API Adapter: {type(container.api_adapter).__name__}')
    print(f'Excel Repository: {type(container.excel_repository).__name__}')
    print(f'Cache: {type(container.cache).__name__}')
except Exception as e:
    print(f'Erro: {e}')
    import traceback
    traceback.print_exc()