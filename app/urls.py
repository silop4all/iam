from django.conf.urls import patterns, url, include
from app.views import *


# Endpoints for views
endpoints = patterns(
    '',
    url(r'^signup-request/$',                                           EmailForm.as_view(),                                    name='signup_request_form'), 
    url(r'^signup/$',                                                   RegistrationView.as_view(),                             name='signup_form'), 
    url(r'^login/$',                                                    LoginView.as_view(),                                    name='login_form'), 
    url(r'^index/$',                                                    DashboardView.as_view(),                                name='dashboard_form'), 
    url(r'^profile/$',                                                  ProfileView.as_view(),                                  name='profile_preview'), 
    url(r'^profile/change-password/$',                                  ProfileChangePwdView.as_view(),                         name='profile_change_pwd'), 
    url(r'^profile/edit/$',                                             ProfileUpdateView.as_view(),                            name='profile_update'), 
    url(r'^applications/$',                                             ApplicationListView.as_view(),                          name='applications_form'), 
    url(r'^applications/register/$',                                    ApplicationCreateView.as_view(),                        name='application_form'), 
    url(r'^applications/(?P<clientId>[0-9a-zA-Z-]+)/$',                 ApplicationPreView.as_view(),                           name='application_info_form'), 
    url(r'^applications/(?P<clientId>[0-9a-zA-Z-]+)/edit/$',            ApplicationUpdateView.as_view(),                        name='application_edit_form'), 
    url(r'^applications/(?P<clientId>[0-9a-zA-Z-]+)/roles/$',           ApplicationRolesView.as_view(),                         name='application_role_form'), 
    url(r'^applications/(?P<clientId>[0-9a-zA-Z-]+)/members/$',         ApplicationAuthMembersView.as_view(),                   name='application_auth_members_form'), 
    url(r'^authorized-applications/overview/$',                         ApplicationsListView.as_view(),                         name='list_applications_form'), 
    url(r'^authorized-applications/(?P<clientId>[0-9a-zA-Z-]+)/roles/$',AuthorizedApplicationRolesView.as_view(),               name='authorized_application_role_form'), 
    url(r'^authorized-applications/access/$',                           AuthorizedApplicationsView.as_view(),                   name='authorized_applications_form'), 
    url(r'^oauth2/authorize/$',                                         AuthorizeApplicationView.as_view(),                     name='authorize_app_form'),

)

# Private API
private_api = patterns(
    '',
    url(r'^iam/openam/authenticate$',                                   MemberAuthentication.as_view({"post": "create"}),                       name='authenticate_url'), 
    url(r'^iam/openam/prepare/register$',                               PrepareRegistration.as_view({'post': 'create'}),                        name='pre_registration_url'), 
    url(r'^iam/openam/users$',                                          MembersListAPIView.as_view({'post': 'create', "get": "retrieve"}),      name='users_url'),
    url(r'^iam/openam/users/(?P<username>[a-zA-Z0-9]+)$',               Members.as_view({"put": 'update'}),                                     name='user_url'),
    url(r'^iam/openam/users/(?P<username>[a-zA-Z0-9]+)/logo$',          UploadUserLogo.as_view(),                                               name="user_logo"), 
    url(r'^iam/openam/users/(?P<username>[a-zA-Z0-9]+)/password$',      MemberChangePasswordAPIView.as_view({"put": 'update'}),                 name='change_password_url'),
    url(r'^iam/openam/requests$',                                       Requests.as_view({"get": "retrieve"}),                                  name='requests_url'),
    url(r'^iam/openam/logout$',                                         Logout.as_view({"get": "retrieve"}),                                    name='logout_url'), 
    url(r'^iam/openam/authorize$',                                      ClientAuthorization.as_view({"get": "retrieve"}),                       name='authorize_url'), 
    url(r'^iam/openam/roles$',                                          GenericRolesListAPIView.as_view({"post": "create", "get": "retrieve"}), name='add_role_url'), 
    url(r'^iam/openam/applications$',                                   ClientsList.as_view({"post": "create", "get": "retrieve"}),             name='application_url'), 
    url(r'^iam/openam/applications/(?P<clientId>[0-9a-zA-Z-]+)$',       ApplicationAPIView.as_view({"put":"update", "delete": "destroy"}),      name='update_application_url'), 
    url(r'^iam/openam/applications/(?P<clientId>[0-9a-zA-Z-]+)/roles$', ApplicationRolesAPIView.as_view({"put":"update"}),                      name='set_application_role_url'), 
    url(r'^iam/openam/authorized-applications/(?P<clientId>[0-9a-zA-Z-]+)/users/(?P<username>[a-zA-Z0-9]+)$',      ApplicationMemberAPIView.as_view({"post":"create", "delete": "destroy"}),   name='set_application_member_url'), 
    url(r'^iam/openam/authorized-applications/(?P<clientId>[0-9a-zA-Z-]+)/users/(?P<username>[a-zA-Z0-9]+)/roles$',ApplicationMemberHasRoleAPIView.as_view({"put":"update"}),                  name='set_member_application_roles_url'), 
    url(r'^iam/openam/authorized-applications/tokens$',                 ActiveAccessTokenListAPIView.as_view({"get": "retrieve"}),              name='access_tokens_url'), 
    url(r'^iam/openam/authorized-applications/tokens/(?P<id>[0-9a-zA-Z-]+)$',ActiveAccessTokenAPIView.as_view({"delete": "destroy"}),           name='access_token_url'), 
    url(r'^iam/oauth2/authorize$',                                      DirectClientAuthorization.as_view({"post": "create"}),                  name='authorize_direct_app_url'),


    # endpoints
    url(r'^roles$',        RolesList.as_view(),                                    name='roles_url'), 
    url(r'^users/(?P<username>[a-zA-Z0-9]+)/applications$',        MyApplicationsList.as_view(),                           name='my_applications_url'), 
)