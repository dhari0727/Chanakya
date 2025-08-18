# Overview

This is a Google Search clone web application that mimics the appearance and basic functionality of Google's search interface. The application features a homepage with the iconic Google logo and search bar, plus a search results page that displays mock data. It's built as a simple demonstration of web development skills, focusing on frontend design and user experience rather than actual search functionality.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses a traditional server-side rendered architecture with Flask templates and Bootstrap for styling. The frontend consists of two main pages: a homepage with a centered search interface that closely mimics Google's design, and a search results page that displays paginated mock results. The UI leverages Bootstrap 5 for responsive design and Font Awesome for icons, with custom CSS to achieve Google's distinctive visual styling including the multicolored logo and clean search interface.

## Backend Architecture
Built on Flask, a lightweight Python web framework, the backend follows a simple MVC pattern. The main application logic is contained in `app.py` with route handlers for the homepage and search functionality. The application uses file-based data storage with JSON files for mock search results and search suggestions, rather than a database. This keeps the architecture simple while demonstrating core web development concepts like routing, templating, and data handling.

## Data Storage
The application uses static JSON files stored in the `static/data/` directory for all data needs. `mock_results.json` contains sample search results with titles, URLs, domains, and snippets, while `suggestions.json` holds predefined search suggestions. This file-based approach eliminates the need for database setup while still providing realistic search functionality for demonstration purposes.

## Search Functionality
The search system implements basic text matching against the mock data, filtering results based on whether the search query appears in result titles or snippets. If no specific matches are found, it defaults to showing general results. The system includes pagination with 10 results per page and maintains search state through URL parameters, providing a realistic search experience despite using static data.

## User Interface Components
The frontend implements key Google Search features including autocomplete suggestions with keyboard navigation (arrow keys, enter, escape), a search input with microphone and camera icons for visual completeness, and responsive design that works across different screen sizes. The search suggestions dropdown provides real-time feedback as users type, enhancing the authentic Google search experience.

# External Dependencies

## Frontend Libraries
- **Bootstrap 5.3.0**: Provides responsive grid system, form styling, and utility classes for consistent UI components across the application
- **Font Awesome 6.4.0**: Supplies vector icons for search, microphone, camera, and other interface elements that match Google's visual design

## Python Framework
- **Flask**: Lightweight web framework handling routing, templating, and request/response processing for the server-side application logic

## Static Assets
- **Mock Data Files**: JSON files containing search results and suggestions data that simulate real search functionality without requiring external APIs or databases
- **Custom CSS/JavaScript**: Application-specific styling and interactive features that recreate Google's distinctive look and feel, including the multicolored logo and search suggestions behavior