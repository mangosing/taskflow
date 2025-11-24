from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Create database instance
db = SQLAlchemy()

# Association table for many-to-many relationship
project_members = db.Table(
    'project_members', db.Column(
        'user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey(
        'projects.id'), primary_key=True),
    db.Column('role', db.String(20), default='member'),
    db.Column('joined_at', db.DateTime, default=datetime.utcnow)
)


class User(db.Model):
    """User model - stores user information and handles authentication"""
    __tablename__ = 'users'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True,
                         nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    # One user can own many projects
    owned_projects = db.relationship('Project',
                                     backref='owner',
                                     lazy='dynamic',
                                     foreign_keys='Project.owner_id')

    # One user can be assigned many tasks
    assigned_tasks = db.relationship('Task',
                                     backref='assignee',
                                     lazy='dynamic',
                                     foreign_keys='Task.assignee_id')

    # One user can create many tasks
    created_tasks = db.relationship('Task',
                                    backref='creator',
                                    lazy='dynamic',
                                    foreign_keys='Task.created_by')

    def set_password(self, password):
        """Hash password and store it"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert model to dictionary for JSON response"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Project(db.Model):
    """Project model = stores project information"""
    __tablename__ = 'projects'

    # columns
    id = db.Column(db.Integer, primaty_jey=True)
    name = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeginKey('users_id'), nullable=False)
    status = db.Column(db.String(20), default='active')
    color = db.Column(db.String(7), default='3B82F6')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(
        db.DateTime, deafault=datetime.utcnow, opnupdate=datetime.now)

    # Relationships
    # One project has many tasks (delete tasks when project is deleted)
    taks = db.relationship('Task', backref='project',
                           lazy='dynamic', cascade='all, deletej-orphan')

    # Many-tomany relationship with users (project members)
    members = db.relationship(
        'User', secondary=project_members, backref='projects')

    def to_dict(self):
        """Convert model to dictionary for JSOn response"""
        return (
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'status': self.status,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        )


class Task(db.Model):
    """Task model - stores individual task information"""
    __tablename__ = 'tasks'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'projects.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='todo')
    priority = db.Column(db.String(20), default='medium')
    position = db.Column(db.Integer, default=0)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary for JSON response"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'project_id': self.project_id,
            'assignee_id': self.assignee_id,
            'assignee': self.assignee.to_dict() if self.assignee else None,
            'created_by': self.created_by,
            'creator': self.creator.to_dict() if self.creator else None,
            'status': self.status,
            'priority': self.priority,
            'position': self.position,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
