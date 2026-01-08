from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from backend import db
from backend.models.user_model import User, MedicalHistory
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    if current_user.role == 'doctor':
        return redirect(url_for('dashboard.doctor_dashboard'))
    return redirect(url_for('dashboard.patient_dashboard'))

@dashboard_bp.route('/patient/dashboard', methods=['GET', 'POST'])
@login_required
def patient_dashboard():
    if current_user.role != 'patient':
        abort(403) # Forbidden
    
    history = current_user.medical_history

    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        blood_group = request.form.get('blood_group')
        allergies = request.form.get('allergies')
        chronic_diseases = request.form.get('chronic_diseases')
        past_surgeries = request.form.get('past_surgeries')
        current_medications = request.form.get('current_medications')
        family_history = request.form.get('family_history')

        if history:
            # Update existing
            history.age = age
            history.gender = gender
            history.blood_group = blood_group
            history.allergies = allergies
            history.chronic_diseases = chronic_diseases
            history.past_surgeries = past_surgeries
            history.current_medications = current_medications
            history.family_history = family_history
            history.updated_at = datetime.utcnow()
        else:
            # Create new
            history = MedicalHistory(
                user_id=current_user.id,
                age=age,
                gender=gender,
                blood_group=blood_group,
                allergies=allergies,
                chronic_diseases=chronic_diseases,
                past_surgeries=past_surgeries,
                current_medications=current_medications,
                family_history=family_history
            )
            db.session.add(history)
        
        db.session.commit()
        flash('Medical History Updated Successfully!', 'success')
        return redirect(url_for('dashboard.patient_dashboard'))

    return render_template('dashboard/patient_dashboard.html', history=history)

@dashboard_bp.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        abort(403)
    
    patients = User.query.filter_by(role='patient').all()
    # Eager load history or join query could be better for performance, but lazy load is fine for now
    
    return render_template('dashboard/doctor_dashboard.html', patients=patients)
