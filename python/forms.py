# forms.py
from flask_wtf import FlaskForm
from wtforms import Form, HiddenField, DateTimeField, StringField, PasswordField, BooleanField, IntegerField, DecimalField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired
from datetime import datetime

class IndexForm(Form):
    pass

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    
class GpioForm(Form):
    pass    
    

class MusicSearchForm(Form):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Publisher', 'Publisher')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')
    
class AlbumForm(Form):
    media_types = [('Digital', 'Digital'),
                   ('CD', 'CD'),
                   ('Cassette Tape', 'Cassette Tape')
                   ]
    artist = StringField('Artist')
    title = StringField('Title')
    release_date = StringField('Release Date')
    publisher = StringField('Publisher')
    media_type = SelectField('Media', choices=media_types)
    
class PhenoForm(FlaskForm):
    tm = datetime.utcnow()    
    # Timestamp
    # Field
    # Trial
    # Plot (plant)
    # Participant
    # Comment
    subject_types = [('Plant', 'Plant'),
                   ('Leaf', 'Leaf'),
                   ('Root', 'Root')
                   ]
    attribute_types = [('Height', 'Height'),
                   ('Legth', 'Length'),
                   ('Width', 'Width'),
                   ('Weight', 'Weight') 
                   ]
    units_types = [('mm', 'mm'),
                   ('g', 'grams')
                  ]      
    timestamp = DateTimeField('Timestamp YYYY-MM-DDTHH:MM:SS', validators=[DataRequired()], format='%Y-%m-%dT%H:%M:%S', default=tm)
    field = HiddenField('Field')
    trial = HiddenField('Trial')
    plot = IntegerField('Plot')
    subject = SelectField('Subject', choices=subject_types, default='Plant')
    attribute = SelectField('Attribute', choices=attribute_types, default='Height')           
    value = DecimalField('Value', validators=[DataRequired()])
    units = SelectField('Units', choices=units_types, default = 'mm')
    participant = StringField('Participant', validators=[DataRequired()])
    comment = StringField('Comment')
    save_more = SubmitField('Save and Add')
    save_exit = SubmitField('Save and Exit')
    cancel = SubmitField('Cancel')    
    
class Test2(FlaskForm):
    #tm = datetime.utcnow().isoformat()[:19]
    tm = datetime.utcnow()    
    ts = DateTimeField('Timestamp YYYY-MM-DDTHH:MM:SS', validators=[DataRequired()], format='%Y-%m-%dT%H:%M:%S', default=tm)
    #ts = DateTimeField('Timestamp YYYY-MM-DDTHH:MM:SS', validators=[DataRequired()], format='%Y-%m-%dT%H:%M:%S')    
    username = StringField('Username', validators=[DataRequired()], default='Phred')
    submit = SubmitField('Do It')
    pass
     