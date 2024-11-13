# PropertyConnect Core Functions

## Description

PropertyConnect Core Functions is a collection of Firebase Cloud Functions designed to handle backend operations for the PropertyConnect application. These functions include user authentication, data management, and other server-side logic necessary for the app's functionality.

## Prerequisites

- Node.js
- npm

## Installation - Firebase

1. **Install Firebase Tools:**

   ```sh
   npm install -g firebase-tools
   ```

2. **Login to Firebase:**

   ```sh
   firebase login
   ```

3. **Initialize Firebase in your project:**
   ```sh
   firebase init
   ```

## Running Firebase Functions Locally

1. **Navigate to your functions directory:**

   ```sh
   cd functions
   ```

2. **Install dependencies:**

   ```sh
   npm install
   ```

3. **Run Firebase functions locally:**

   ```sh
   firebase emulators:start
   ```

4. **Deploy Firebase functions:**
   ```sh
   firebase deploy --only hosting
   ```
   This will start the Firebase emulator suite, allowing you to test your functions locally.
