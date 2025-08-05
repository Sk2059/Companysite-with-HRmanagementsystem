# CliCK DIGITALS - Digital Services & Career Platform

A comprehensive Django-based web platform that serves as both a digital services company website and career management system. CliCK DIGITALS offers web development and digital marketing services while providing a complete recruitment and employee management solution.

## 🚀 Features

### 🏢 Service Portfolio
- **Web Development Services**: Custom web applications, responsive design, and full-stack solutions
- **Digital Marketing**: SEO, social media marketing, content strategy, and online advertising
- **Combo Packages**: Integrated development and marketing solutions
- **Project Management**: End-to-end project tracking from client inquiry to completion

### 👥 Career Management
- **Job Vacancy System**: Post internships and full-time positions (Junior/Senior levels)
- **Applicant Tracking**: Resume uploads, skill assessment, and application management
- **Interview Scheduling**: Automated interview scheduling and candidate communication
- **Employee Management**: Complete CRUD operations with performance tracking

### 📚 Educational Platform
- **Course Offerings**: Web Development, Digital Marketing, Data Science, UI/UX Design
- **Multiple Learning Modes**: Online, Offline, and Hybrid options
- **Registration System**: Course enrollment with detailed student information
- **Skill Development**: Beginner to Advanced level courses

### 📝 Content & Collaboration
- **Blog System**: Industry insights with author profiles and keyword tagging
- **Business Partnerships**: Collaboration inquiry system for potential clients
- **Testimonials**: Client feedback and success stories
- **Contact Management**: Inquiry handling and communication tracking

## 🛠️ Tech Stack

- **Backend**: Django 5.1.2
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **File Handling**: Media uploads for resumes, portfolios, images
- **Email**: SMTP integration for notifications
- **Authentication**: Django built-in authentication system

## 📋 Prerequisites

- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)
- Virtual environment (recommended)

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd server
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   - Create a MySQL database named `test_db`
   - Update database credentials in `server/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'test_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': '127.0.0.1',
           'PORT': '3306'
       }
   }
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to access the application.

## 📁 Project Structure

```
server/
├── app/                    # Main application views and templates
├── blog/                   # Blog management system
├── collab/                 # Business collaboration features
├── course/                 # Educational platform
├── myapp/                  # Employee management
├── projects/               # Service and project management
├── vacancy/                # Job posting and applicant tracking
├── media/                  # User uploaded files
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # HTML templates
├── server/                 # Django project settings
└── manage.py              # Django management script
```

## 🔧 Configuration

### Email Settings
Update email configuration in `server/settings.py`:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### Media Files
Ensure media directory has proper permissions for file uploads:
- Employee images
- Applicant resumes
- Blog photos
- Service images

## 🚀 Usage

### Admin Panel
Access the Django admin at `http://127.0.0.1:8000/admin/` to:
- Manage employees and skills
- Create job vacancies
- Review applications
- Manage courses and registrations
- Handle blog posts and content

### Main Features Access
- **Home**: `/` - Main landing page with services and opportunities
- **Services**: `/services/` - Browse available services
- **Careers**: `/careers/` - View job openings and internships
- **Courses**: `/courses/` - Educational offerings
- **Blog**: `/blogs/` - Industry insights and articles
- **Contact**: `/contact/` - Get in touch form

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and inquiries:
- Email: clickdigitals2024@gmail.com
- Website: https://clickdigitals.com.np

## 🔮 Future Enhancements

- Payment gateway integration for courses
- Real-time chat support
- Advanced analytics dashboard
- Mobile application
- API development for third-party integrations
- Multi-language support

---

**Built with ❤️ by CliCK DIGITALS Team**
