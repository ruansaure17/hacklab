# Architecture

## Overview

HackLab is a deliberately vulnerable web application designed for educational purposes.

The application is built using:

* Flask
* SQLite
* HTML/CSS
* JavaScript

## Components

### Authentication

Handles user registration, login, and session management.

### User Profiles

Allows users to view and update profile information.

### Search Module

Provides content discovery functionality.

### Upload System

Handles user-submitted files.

### Administrative Panel

Provides privileged functionality for administrative users.

### API Layer

Exposes application data through HTTP endpoints.

## Database

SQLite is used as the primary datastore.

Main entities include:

* Users
* Posts
* Comments
* Uploaded Files

## Deployment

The application can be deployed locally using:

* Python
* Docker
* Docker Compose
