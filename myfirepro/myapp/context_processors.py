def user_email(request):
    return {
        "email": request.session.get("email")
    }
