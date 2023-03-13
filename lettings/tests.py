import pytest
from django.urls import reverse
from django.test import Client
from .models import Letting, Address
from pytest_django.asserts import assertTemplateUsed, assertQuerysetEqual


@pytest.mark.django_db
def test_index_view():
    client = Client()
    address_1 = Address.objects.create(number=250, street="Saint-Mary",
                                       city="Chicago", state="Illinois",
                                       zip_code=309, country_iso_code="USA")
    address_2 = Address.objects.create(number=100, street="Pierre-fonds",
                                       city="San Francisco", state="California",
                                       zip_code=500, country_iso_code="USA")
    address_3 = Address.objects.create(number=60, street="Glenwood",
                                       city="New York City", state="New York",
                                       zip_code=101, country_iso_code="USA")
    letting_1 = Letting.objects.create(title="The crystal palace", address=address_1)
    letting_2 = Letting.objects.create(title="Yan's manor", address=address_2)
    letting_3 = Letting.objects.create(title="Al Riyad", address=address_3)
    lettings_list = [letting_1, letting_2, letting_3]
    path = reverse("lettings:index")
    response = client.get(path)
    content = response.content.decode()
    expected_content = '<title>Lettings</title>\n' \
                       '<h1>Lettings</h1>\n' \
                       '\n' \
                       '    <ul>\n' \
                       '    \n' \
                       '        <li>\n ' \
                       '           <a href="/lettings/1/">\n ' \
                       '               The crystal palace\n ' \
                       '           </a>\n' \
                       '        </li>\n ' \
                       '   \n ' \
                       '       <li>\n ' \
                       '           <a href="/lettings/2/">\n  ' \
                       '              Yan&#x27;s manor\n  ' \
                       '          </a>\n   ' \
                       '     </li>\n' \
                       '    \n ' \
                       '       <li>\n ' \
                       '           <a href="/lettings/3/">\n    ' \
                       '            Al Riyad\n  ' \
                       '          </a>\n   ' \
                       '     </li>\n ' \
                       '   \n ' \
                       '   </ul>\n' \
                       '\n' \
                       '<div><a href="/">Home</a></div>\n' \
                       '<div><a href="/profiles/">Profiles</a></div>'

    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response, "lettings/index.html")
    assertQuerysetEqual(response.context['lettings_list'], lettings_list, ordered=False)


@pytest.mark.django_db
def test_letting_view():
    client = Client()
    address = Address.objects.create(number=250, street="Saint-Mary",
                                     city="Chicago", state="Illinois",
                                     zip_code=309, country_iso_code="USA")
    letting = Letting.objects.create(title="The crystal palace", address=address)
    path = reverse("lettings:letting", kwargs={"letting_id": letting.pk})
    response = client.get(path)
    content = response.content.decode()
    expected_content = '<title>The crystal palace</title>\n' \
                       '<h1>The crystal palace</h1>\n' \
                       '<p>250 Saint-Mary</p>\n' \
                       '<p>Chicago, Illinois 309</p>\n' \
                       '<p>USA</p>\n' \
                       '<div><a href="/lettings/">Back</a></div>\n' \
                       '<div><a href="/">Home</a></div>\n' \
                       '<div><a href="/profiles/">Profiles</a></div>'

    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response, "lettings/letting.html")
