from .models import AppUser

def capitalize_country_names():
    users = AppUser.objects.all()  # Fetch all users
    updated_count = 0  # Counter for updated records

    for user in users:
        if user.country:  # Ensure the country field is not None
            capitalized_country = user.country.title()  # Capitalize the country name
            if capitalized_country != user.country:  # Only update if there's a change
                user.country = capitalized_country
                user.save()
                print(updated_count)  # Save the user record
                updated_count += 1  # Increment the updated counter

    print(f"Updated {updated_count} user(s) with capitalized country names.")

# Run the function in the shell
if __name__ == "__main__":
    capitalize_country_names()
