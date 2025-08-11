from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from config import Config
from models import db, Guest, Room, Booking, Service, Staff
from forms import GuestForm, BookingForm
from io import StringIO
import csv

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Initialize DB tables if not using migrations (careful: won't preserve data if drop)
    # with app.app_context():
    #     db.create_all()

    @app.route("/")
    def index():
        return redirect(url_for('guest_list'))

    # ---------- Guest CRUD ----------
    @app.route("/guests")
    def guest_list():
        guests = Guest.query.order_by(Guest.id.desc()).all()
        return render_template("guests/list.html", guests=guests)

    @app.route("/guests/add", methods=["GET", "POST"])
    def guest_add():
        form = GuestForm()
        if form.validate_on_submit():
            g = Guest(fullname=form.fullname.data, contact=form.contact.data)
            db.session.add(g)
            db.session.commit()
            flash("Guest added", "success")
            return redirect(url_for('guest_list'))
        return render_template("guests/form.html", form=form, action="Add")

    @app.route("/guests/edit/<int:id>", methods=["GET","POST"])
    def guest_edit(id):
        g = Guest.query.get_or_404(id)
        form = GuestForm(obj=g)
        if form.validate_on_submit():
            g.fullname = form.fullname.data
            g.contact = form.contact.data
            db.session.commit()
            flash("Guest updated", "success")
            return redirect(url_for('guest_list'))
        return render_template("guests/form.html", form=form, action="Edit")

    @app.route("/guests/delete/<int:id>", methods=["POST"])
    def guest_delete(id):
        g = Guest.query.get_or_404(id)
        db.session.delete(g)
        db.session.commit()
        flash("Guest deleted", "success")
        return redirect(url_for('guest_list'))

    # ---------- Rooms ----------
    @app.route("/rooms")
    def rooms():
        rooms = Room.query.all()
        return render_template("rooms/list.html", rooms=rooms)

    # ---------- Booking ----------
    @app.route("/bookings")
    def bookings():
        bookings = Booking.query.order_by(Booking.date.desc()).all()
        return render_template("bookings/list.html", bookings=bookings)

    @app.route("/bookings/add", methods=["GET","POST"])
    def booking_add():
        form = BookingForm()
        form.guest_id.choices = [(g.id, g.fullname) for g in Guest.query.all()]
        form.room_id.choices = [(r.id, f"{r.id} - {r.room_type} ({r.room_status})") for r in Room.query.filter_by(room_status='Free').all()]
        if form.validate_on_submit():
            b = Booking(guest_id=form.guest_id.data, room_id=form.room_id.data)
            # mark room as Booked
            room = Room.query.get(form.room_id.data)
            room.room_status = 'Booked'
            db.session.add(b)
            db.session.commit()
            flash("Room booked", "success")
            return redirect(url_for('bookings'))
        return render_template("bookings/form.html", form=form)

    # Checkout: mark room free and optionally delete booking or keep record
    @app.route("/bookings/checkout/<int:id>", methods=["POST"])
    def booking_checkout(id):
        b = Booking.query.get_or_404(id)
        room = Room.query.get(b.room_id)
        room.room_status = 'Free'
        # you can delete booking or set checkout date field (not in current schema)
        db.session.delete(b)
        db.session.commit()
        flash("Checked out", "success")
        return redirect(url_for('bookings'))

    # ---------- Reports (simple CSV) ----------
    @app.route("/reports/guests.csv")
    def report_guests_csv():
        guests = Guest.query.all()
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['id','fullname','contact','date'])
        for g in guests:
            cw.writerow([g.id, g.fullname, g.contact, g.date])
        output = si.getvalue()
        return send_file(
            StringIO(output),
            mimetype='text/csv',
            as_attachment=True,
            download_name='guests.csv'
        )

    @app.route("/reports/summary")
    def report_summary():
        total_guests = Guest.query.count()
        total_rooms = Room.query.count()
        booked_rooms = Room.query.filter_by(room_status='Booked').count()
        return render_template("reports.html", total_guests=total_guests,
                               total_rooms=total_rooms, booked_rooms=booked_rooms)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
