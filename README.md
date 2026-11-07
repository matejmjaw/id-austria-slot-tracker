# Open ID Austria Appointment Tracker

An automated, serverless monitor that checks for open ID Austria registration slots across Vienna police stations and emails alerts immediately when an early cancellation is detected.

## Setup Instructions

1. **Gmail App Password**: Ensure 2-Step Verification is enabled on your Google account, generate an **App Password**, and copy the 16-character code.
2. **Repository Secrets**: Add the following secrets under your repository **Settings > Secrets and variables > Actions**:
   - `EMAIL_USER`: Your full Gmail address.
   - `EMAIL_PASS`: Your 16-character Gmail App Password.
   - `USER_LASTNAME`: `coyote` (or any dummy text)
   - `USER_FIRSTNAME`: `wile-e` (or any dummy text)
   - `USER_DOB`: `01.01.2000`
   - `USER_EMAIL`: Your receiving email address.
