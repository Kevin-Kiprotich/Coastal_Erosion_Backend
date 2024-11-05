from django.db import models
from collections import Counter
from .models import AppUser, CountryCount, SectorCount, InstitutionCount, RoleCount, MonthlyUserRegistration

def update_statistics():
    # Count users by country, sector, institution, and role
    users = AppUser.objects.all()
    
    # Create counters
    country_counts = Counter(users.values_list('country', flat=True))
    sector_counts = Counter(filter(None, users.values_list('sector', flat=True)))
    institution_counts = Counter(filter(None, users.values_list('institution', flat=True)))
    role_counts = Counter(filter(None, users.values_list('role', flat=True)))

    # Update or create CountryCount records
    for country, count in country_counts.items():
        country_stat, _ = CountryCount.objects.get_or_create(country=country)
        country_stat.user_count = count
        country_stat.save()

    # Update or create SectorCount records
    for sector, count in sector_counts.items():
        sector_stat, _ = SectorCount.objects.get_or_create(sector=sector)
        sector_stat.user_count = count
        sector_stat.save()

    # Update or create InstitutionCount records
    for institution, count in institution_counts.items():
        institution_stat, _ = InstitutionCount.objects.get_or_create(institution=institution)
        institution_stat.user_count = count
        institution_stat.save()

    # Update or create RoleCount records
    for role, count in role_counts.items():
        role_stat, _ = RoleCount.objects.get_or_create(role=role)
        role_stat.user_count = count
        role_stat.save()

    # Monthly registration counts based on date_joined
    monthly_counts = (
        users
        .values('date_joined__year', 'date_joined__month')
        .annotate(registration_count=models.Count('id'))
    )

    # Month mapping from numbers to words
    month_mapping = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    for item in monthly_counts:
        month_number = item['date_joined__month']
        year = item['date_joined__year']
        
        # Convert month number to month name
        month_name = month_mapping.get(month_number)
        
        # Get or create the monthly registration record for each month/year combination
        monthly_stat, _ = MonthlyUserRegistration.objects.get_or_create(
            month=month_name,  # Use the month name
            year=year
        )
        
        monthly_stat.registration_count = item['registration_count']
        monthly_stat.save()

    print("Successfully updated statistics for all existing users.")

# Run the function in the shell
if __name__ == "__main__":
    update_statistics()
