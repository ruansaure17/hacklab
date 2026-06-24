# Solutions Guide

⚠️ Spoiler Warning

This document contains information about the intentionally vulnerable components included in HackLab.

If you want the full challenge experience, stop reading here.

---

# Overview

HackLab was intentionally designed with multiple security flaws inspired by real-world vulnerabilities frequently observed during web application assessments.

The goal is to help students develop:

* Vulnerability discovery skills
* Security testing methodology
* Risk assessment capabilities
* Remediation planning

---

# Vulnerability Categories

## 1. Injection

### Description

The application contains functionality that fails to properly separate user input from backend processing logic.

### Learning Objectives

* Understand insecure input handling
* Learn how injection flaws occur
* Recognize the importance of parameterized queries

### OWASP Category

Injection

---

## 2. Broken Access Control

### Description

Certain application features fail to properly enforce authorization checks.

Users may be able to access resources that should be restricted to other users.

### Learning Objectives

* Differentiate authentication from authorization
* Identify missing ownership validation
* Understand horizontal and vertical privilege escalation

### OWASP Category

Broken Access Control

---

## 3. API Authorization Issues

### Description

Some API endpoints expose information that should require additional access control validation.

### Learning Objectives

* Test API security
* Identify insecure direct object references
* Understand data exposure risks

### OWASP Category

Broken Access Control

---

## 4. Cross-Site Scripting (XSS)

### Description

User-controlled content may be rendered in the browser without proper output encoding.

### Learning Objectives

* Understand reflected and stored XSS
* Learn browser-side attack surfaces
* Recognize the importance of output sanitization

### OWASP Category

Injection

---

## 5. Insecure File Handling

### Description

The application includes functionality that processes user-controlled file names and uploaded content.

### Learning Objectives

* Assess upload functionality
* Analyze file access controls
* Understand risks related to unsafe file processing

### OWASP Category

Security Misconfiguration

---

## 6. Sensitive Information Exposure

### Description

Application data and configuration details may be exposed through insecure implementation choices.

### Learning Objectives

* Identify exposed secrets
* Review application configuration
* Evaluate information disclosure impact

### OWASP Category

Security Misconfiguration

---

## 7. Weak Cryptography

### Description

Some security-sensitive operations rely on outdated or insufficient cryptographic approaches.

### Learning Objectives

* Understand password storage risks
* Evaluate cryptographic decisions
* Learn modern password hashing recommendations

### OWASP Category

Cryptographic Failures

---

## 8. Cross-Site Request Forgery (CSRF)

### Description

Certain state-changing operations do not implement request origin validation.

### Learning Objectives

* Understand CSRF attack scenarios
* Learn anti-CSRF protection mechanisms
* Evaluate browser trust assumptions

### OWASP Category

Broken Access Control

---

# Recommended Remediations

Students are encouraged to create a secure version of the application by implementing:

* Parameterized database queries
* Proper authorization checks
* Output encoding and sanitization
* Secure file upload validation
* Path validation and normalization
* CSRF protection
* Strong password hashing
* Secure secret management
* Principle of least privilege

---

# Secure Version Challenge

As a follow-up exercise, create a second branch named:

```text
secure
```

and fix every identified vulnerability while maintaining the same application features.

This exercise helps bridge the gap between offensive and defensive security practices.

---

# Final Goal

The purpose of HackLab is not only to find vulnerabilities, but also to understand:

* Why they exist
* How they are exploited
* How they can be prevented
* How secure software should be designed

Happy hacking and happy learning.
