from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import requests
from ipware import get_client_ip
from django.template.exceptions import TemplateDoesNotExist
from django.core.exceptions import PermissionDenied

from .forms import PluginSettingsForm
from .models import PluginSettings

@login_required
@permission_required('aa_proxy_reg.change_pluginsettings')
def settings_view(request):
    try:
        instance = PluginSettings.objects.get(pk=1)
    except PluginSettings.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form = PluginSettingsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Настройки успешно сохранены!')
            return redirect('aa_proxy_reg:settings')
    else:
        form = PluginSettingsForm(instance=instance)

    context = {
        'form': form,
        'page_title': 'Настройки плагина ProxyReg'
    }
    return render(request, 'aa_proxy_reg/settings.html', context)


@login_required
def main_view(request):
    try:
        if not request.user.groups.filter(name='Verified').exists():
            raise PermissionDenied("У вас нет доступа к этому плагину")
        
        return render(request, 'aa_proxy_reg/main.html')
    except TemplateDoesNotExist as e:
        logger.error(f"Template not found: {e}")
        return JsonResponse(
            {'status': 'error', 'message': 'Template not found'},
            status=500
        )



@login_required
@require_http_methods(["POST"])
def call_api_endpoint(request):
    # Get user IP address
    client_ip, is_routable = get_client_ip(request)
    settings = PluginSettings.get_settings()
    
    if client_ip is None:
        return JsonResponse(
            {'status': 'error', 'message': 'Could not get client IP'},
            status=400
        )
    
    # Get character name from auth
    character_name = request.user.profile.main_character.character_name
    
    # Get API key from user settings (you'll need to implement this)
    try:
        api_key = settings.api_key
    except AttributeError:
        return JsonResponse(
            {'status': 'error', 'message': 'API key not configured'},
            status=400
        )
    
    # Prepare API request
    api_url = settings.api_endpoint  # Replace with your API URL
    params = {
        'ipAddress': client_ip,
        'characterName': character_name,
        'apiKey': api_key
    }
    
    try:
        response = requests.post(api_url, json=params, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {'status': 'error', 'message': str(e)},
            status=500
        )