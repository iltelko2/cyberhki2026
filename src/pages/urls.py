from django.urls import path

from .views import (
    topicsView, topicView, quizView, answerView, incorrectView, finishView,
    thanksView, cheaterView, securityOverviewView, securityAdminDataView,
    securityCryptoView, securitySearchView, securityLoginView, securityLoggingView
)

urlpatterns = [
    path('', topicsView, name='home'),
    path('topic/<int:tid>/', topicView, name='topic'),
    path('quiz/<int:tid>/', quizView, name='quiz'),
    path('incorrect/', incorrectView, name='wrong'),
    path('finish/', finishView, name='finish'),
    path('thanks/', thanksView, name='thanks'),
    path('cheater/', cheaterView, name='cheater'),
    path('quiz/<int:tid>/<int:aid>/', answerView, name='answer'),
    path('security/', securityOverviewView, name='security-overview'),
    path('security/admin-data/', securityAdminDataView, name='security-admin-data'),
    path('security/crypto/', securityCryptoView, name='security-crypto'),
    path('security/search/', securitySearchView, name='security-search'),
    path('security/login/', securityLoginView, name='security-login'),
    path('security/logging/', securityLoggingView, name='security-logging'),
]
