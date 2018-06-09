# trade/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializers import UserProposalDetailSerializer,UserProposalOptionSerializer,UserProposalOptionDetailSerializer,UserProposalSerializer
from .models import UserProposal,UserProposalOption
from rest_framework import mixins
from django.shortcuts import render, redirect

from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
# todo





