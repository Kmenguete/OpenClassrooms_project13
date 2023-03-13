import pytest
from django.urls import reverse
from django.test import Client
from .models import Profile
from pytest_django.asserts import assertTemplateUsed, assertQuerysetEqual
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_index_view():
    client = Client()
    user_1 = User.objects.create(username="Matthieu", first_name="Matt",
                                 last_name="Jammy", email="mattjam@gmail.com")
    user_2 = User.objects.create(username="Elodie", first_name="Elodie",
                                 last_name="Belem", email="elodiebelem@gmail.com")
    user_3 = User.objects.create(username="Vanessa", first_name="Vanessa",
                                 last_name="Britz", email="vbritz@gmail.com")
    profile_1 = Profile.objects.create(user=user_1, favorite_city="Chicago")
    profile_2 = Profile.objects.create(user=user_2, favorite_city="San Francisco")
    profile_3 = Profile.objects.create(user=user_3, favorite_city="New York City")
    profiles_list = [profile_1, profile_2, profile_3]
    path = reverse("profiles:index")
    response = client.get(path)
    content = response.content.decode()
    expected_content = '<title>Profiles</title>\n' \
                       '<h1>Profiles</h1>\n' \
                       '\n' \
                       '    <ul>\n ' \
                       '   \n' \
                       '        <li>\n ' \
                       '           <a href="/profiles/Matthieu/">\n ' \
                       '               Matthieu\n ' \
                       '           </a>\n' \
                       '        </li>\n' \
                       '    \n ' \
                       '       <li>\n ' \
                       '           <a href="/profiles/Elodie/">\n  ' \
                       '              Elodie\n  ' \
                       '          </a>\n  ' \
                       '      </li>\n' \
                       '    \n  ' \
                       '      <li>\n  ' \
                       '          <a href="/profiles/Vanessa/">\n    ' \
                       '            Vanessa\n   ' \
                       '         </a>\n  ' \
                       '      </li>\n ' \
                       '   \n   ' \
                       ' </ul>\n' \
                       '\n' \
                       '<div><a href="/">Home</a></div>\n' \
                       '<div><a href="/lettings/">Lettings</a></div>'

    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/index.html")
    assertQuerysetEqual(response.context['profiles_list'], profiles_list, ordered=False)


@pytest.mark.django_db
def test_letting_view():
    client = Client()
    user = User.objects.create(username="Matthieu", first_name="Matt",
                               last_name="Jammy", email="mattjam@gmail.com")
    profile = Profile.objects.create(user=user, favorite_city="Seattle")
    path = reverse("profiles:profile", kwargs={"username": profile.user.username})
    response = client.get(path)
    content = response.content.decode()
    expected_content = '<title>Matthieu</title>\n' \
                       '<h1>Matthieu</h1>\n' \
                       '<p>First name: Matt</p>\n' \
                       '<p>Last name: Jammy</p>\n' \
                       '<p>Email: mattjam@gmail.com</p>\n' \
                       '<p>Favorite city: Seattle</p>\n' \
                       '<div><a href="/profiles/">Back</a></div>\n' \
                       '<div><a href="/">Home</a></div>\n' \
                       '<div><a href="/lettings/">Lettings</a></div>'

    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/profile.html")
