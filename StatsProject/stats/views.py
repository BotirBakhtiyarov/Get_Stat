from datetime import datetime
from django.db.models import Sum, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_api_key.permissions import HasAPIKey
from .models import Computer, AppUsage, SystemMetrics
from django.utils import timezone
from datetime import timedelta
from rest_framework.parsers import JSONParser

class SecureDataView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        return Response({"message": "API Key bilan himoyalangan ma'lumot!"})


class DataReceiverView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        try:
            data = request.data
            # Validate required fields
            computer_id = data['computer_id']
            timestamp = datetime.fromisoformat(data['timestamp'])

            # Create/update computer
            computer, _ = Computer.objects.update_or_create(
                computer_id=computer_id,
                defaults={'username': data.get('username', 'Unknown')}
            )

            # Save system metrics
            SystemMetrics.objects.create(
                computer=computer,
                cpu_percent=data['cpu'],
                ram_total=data['ram']['total'],
                ram_used=data['ram']['used'],
                ram_percent=data['ram']['percent'],
                timestamp=timestamp
            )

            # Save app usage
            for app_name, metrics in data['apps'].items():
                AppUsage.objects.create(
                    computer=computer,
                    app_name=app_name,
                    duration=metrics['duration'],
                    cpu_usage=metrics['cpu'],
                    ram_usage=metrics['ram'],
                    timestamp=timestamp
                )

            return Response({"status": "success"}, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({"error": f"Missing key: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StatsView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        time_filter = request.GET.get('time_filter', 'latest')
        computers = Computer.objects.all()
        stats = []

        # Define time cutoff
        now = timezone.now()
        if time_filter == 'latest':
            cutoff = now - timedelta(minutes=5)
        elif time_filter == '1h':
            cutoff = now - timedelta(hours=1)
        elif time_filter == '1d':
            cutoff = now - timedelta(days=1)
        else:
            cutoff = now - timedelta(minutes=5)

        for comp in computers:
            # System metrics (latest)
            system_metrics = comp.systemmetrics_set.filter(timestamp__gte=cutoff)
            cpu_percent = system_metrics.aggregate(avg=Avg('cpu_percent'))['avg'] or 0
            ram_usage = system_metrics.aggregate(avg=Avg('ram_percent'))['avg'] or 0

            # App usage with delta duration calculation
            app_usages = (
                comp.appusage_set
                .filter(timestamp__gte=cutoff)
                .order_by('app_name', 'timestamp')
            )

            app_data = {}
            for usage in app_usages:
                app_name = usage.app_name
                if app_name not in app_data:
                    app_data[app_name] = {
                        'durations': [],
                        'cpu_usage': [],
                        'ram_usage': [],
                        'prev_duration': 0
                    }

                # Calculate delta duration from previous report
                delta = usage.duration - app_data[app_name]['prev_duration']
                if delta < 0:
                    delta = usage.duration  # App restarted

                app_data[app_name]['durations'].append(delta)
                app_data[app_name]['cpu_usage'].append(usage.cpu_usage)
                app_data[app_name]['ram_usage'].append(usage.ram_usage)
                app_data[app_name]['prev_duration'] = usage.duration

            # Build app stats
            apps = []
            for app_name, data in app_data.items():
                total_duration = sum(data['durations'])
                avg_cpu = sum(data['cpu_usage']) / len(data['cpu_usage'])
                avg_ram = sum(data['ram_usage']) / len(data['ram_usage'])

                apps.append({
                    "name": app_name,
                    "duration": total_duration // 60,  # Convert to minutes
                    "cpu": round(avg_cpu, 1),
                    "ram": round(avg_ram, 1)
                })

            stats.append({
                "computer_id": comp.computer_id,
                "username": comp.username,
                "last_seen": timezone.localtime(comp.last_seen),
                "cpu_percent": round(cpu_percent, 1),
                "ram_usage": round(ram_usage, 1),
                "apps": sorted(apps, key=lambda x: x['duration'], reverse=True)
            })

        return Response(stats)