# 🧪 HackLab – Solutions & Security Writeups

This document contains structured writeups of vulnerabilities discovered during the HackLab black-box security exercises.

Unlike traditional step-by-step guides, these solutions are documented as **security investigation reports**, focusing on reasoning, validation, and impact analysis.

---

# ⚠️ Important Note

All vulnerabilities documented here were:
- Discovered in a controlled lab environment
- Identified without prior knowledge of their existence
- Tested and validated manually
- Used strictly for educational purposes

---

# 🧠 Methodology Reminder

Each finding follows the same investigation flow:

1. Reconnaissance
2. Surface analysis
3. Hypothesis testing
4. Exploitation validation
5. Impact confirmation
6. Learning extraction

---

# 🧪 Findings

---

## 🔐 Finding #1 – Authentication / Authorization Weakness (Example Pattern)

### Context
During analysis of the authentication flow, the application issues a token after login and uses it for protected routes.

---

### Observation
- Token is generated after login
- Token is accepted by multiple endpoints
- No clear server-side validation consistency across routes

---

### Hypothesis
There may be a mismatch between client-side trust and server-side authorization enforcement.

---

### Testing Steps
- Captured authentication token after login
- Reused token across restricted endpoints
- Modified role-related attributes inside token payload
- Observed inconsistent authorization behavior

---

### Result
Access to restricted functionality was granted under modified identity context.

---

### Impact
- Broken access control
- Potential privilege escalation
- Trust boundary violation between authentication and authorization layers

---

### Key Learning
- Authentication does not guarantee authorization
- Server-side validation must be enforced on every sensitive endpoint
- Token integrity must be strictly verified

---

## 📂 Finding #2 – Input Handling / Injection Surface (Template Pattern)

### Context
User-controlled input is processed and reflected in application responses.

---

### Observation
- Input is accepted without strict sanitization
- Output reflects user-controlled data in multiple contexts

---

### Hypothesis
Application may be vulnerable to injection-based attacks depending on context handling.

---

### Testing Steps
- Injected controlled payloads into input fields
- Observed response behavior changes
- Tested boundary and encoding variations

---

### Result
Application behavior indicates insufficient input validation.

---

### Impact
- Potential injection vulnerabilities depending on backend context
- Risk of data manipulation or unauthorized execution paths

---

### Key Learning
- Input validation must be context-aware
- Output encoding is critical depending on rendering context

---

## 📁 Finding #3 – File Handling Weakness (Generic Pattern)

### Context
Application includes file upload or file processing functionality.

---

### Observation
- Uploaded files are processed without strict validation
- File metadata is accepted from user input

---

### Hypothesis
Improper file validation may allow unintended file handling behavior.

---

### Testing Steps
- Uploaded different file types
- Modified file extensions and metadata
- Observed storage and processing behavior

---

### Result
File handling logic does not fully enforce strict validation rules.

---

### Impact
- Risk of unsafe file processing
- Potential exposure depending on execution context

---

### Key Learning
- File validation must include type, content, and behavior checks
- Trusting client-provided metadata is unsafe

---

# 🧠 Final Notes

These findings represent **patterns of vulnerability classes**, not isolated issues.

The goal of this lab is not only exploitation, but:
- Understanding system assumptions
- Identifying trust boundaries
- Building structured reasoning in offensive security

---

# 🚀 Overall Learning Outcome

Through this lab, the main improvements developed were:

- Ability to identify unknown attack surfaces
- Structured offensive security thinking
- Validation-based exploitation mindset
- Technical security reporting skills

---

# ⚠️ Disclaimer

All testing was performed in isolated environments intended for security education only.
