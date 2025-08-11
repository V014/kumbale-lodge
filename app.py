from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, Guest, Room, Booking, Service, Staff
from forms import GuestForm, RoomForm, BookingForm, ServiceForm, StaffForm

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    # ---------------- Guests CRUD ----------------
    @app.route("/guests")
    def guest_list():
        guests = Guest.query.all()
        return render_template("guests/list.html", guests=guests)

    @app.route("/guests/add", methods=["GET", "POST"])
    def guest_add():
        form = GuestForm()
        if form.validate_on_submit():
            g = Guest(fullname=form.fullname.data, contact=form.contact.data)
            db.session.add(g)
            db.session.commit()
            flash("Guest added", "success")
            return redirect(url_for("guest_list"))
        return render_template("guests/form.html", form=form, action="Add")

    @app.route("/guests/edit/<int:id>", methods=["GET", "POST"])
    def guest_edit(id):
        g = Guest.query.get_or_404(id)
        form = GuestForm(obj=g)
        if form.validate_on_submit():
            g.fullname = form.fullname.data
            g.contact = form.contact.data
            db.session.commit()
            flash("Guest updated", "success")
            return redirect(url_for("guest_list"))
        return render_template("guests/form.html", form=form, action="Edit")

    @app.route("/guests/delete/<int:id>", methods=["POST"])
    def guest_delete(id):
        g = Guest.query.get_or_404(id)
        db.session.delete(g)
        db.session.commit()
        flash("Guest deleted", "success")
        return redirect(url_for("guest_list"))

    # ---------------- Rooms CRUD ----------------
    @app.route("/rooms")
    def room_list():
        rooms = Room.query.all()
        return render_template("rooms/list.html", rooms=rooms)

    @app.route("/rooms/add", methods=["GET", "POST"])
    def room_add():
        form = RoomForm()
        if form.validate_on_submit():
            r = Room(room_type=form.room_type.data, room_status=form.room_status.data)
            db.session.add(r)
            db.session.commit()
            flash("Room added", "success")
            return redirect(url_for("room_list"))
        return render_template("rooms/form.html", form=form, action="Add")

    @app.route("/rooms/edit/<int:id>", methods=["GET", "POST"])
    def room_edit(id):
        r = Room.query.get_or_404(id)
        form = RoomForm(obj=r)
        if form.validate_on_submit():
            r.room_type = form.room_type.data
            r.room_status = form.room_status.data
            db.session.commit()
            flash("Room updated", "success")
            return redirect(url_for("room_list"))
        return render_template("rooms/form.html", form=form, action="Edit")

    @app.route("/rooms/delete/<int:id>", methods=["POST"])
    def room_delete(id):
        r = Room.query.get_or_404(id)
        db.session.delete(r)
        db.session.commit()
        flash("Room deleted", "success")
        return redirect(url_for("room_list"))

    # ---------------- Bookings CRUD ----------------
    @app.route("/bookings")
    def booking_list():
        bookings = Booking.query.all()
        return render_template("bookings/list.html", bookings=bookings)

    @app.route("/bookings/add", methods=["GET", "POST"])
    def booking_add():
        form = BookingForm()
        form.guest_id.choices = [(g.id, g.fullname) for g in Guest.query.all()]
        form.room_id.choices = [(r.id, f"Room {r.id} - {r.room_type}") for r in Room.query.filter_by(room_status='Free')]
        if form.validate_on_submit():
            b = Booking(guest_id=form.guest_id.data, room_id=form.room_id.data)
            room = Room.query.get(form.room_id.data)
            room.room_status = 'Booked'
            db.session.add(b)
            db.session.commit()
            flash("Booking created", "success")
            return redirect(url_for("booking_list"))
        return render_template("bookings/form.html", form=form, action="Add")

    @app.route("/bookings/edit/<int:id>", methods=["GET", "POST"])
    def booking_edit(id):
        b = Booking.query.get_or_404(id)
        form = BookingForm()
        form.guest_id.choices = [(g.id, g.fullname) for g in Guest.query.all()]
        form.room_id.choices = [(r.id, f"Room {r.id} - {r.room_type}") for r in Room.query.all()]
        if request.method == "GET":
            form.guest_id.data = b.guest_id
            form.room_id.data = b.room_id
        if form.validate_on_submit():
            b.guest_id = form.guest_id.data
            b.room_id = form.room_id.data
            db.session.commit()
            flash("Booking updated", "success")
            return redirect(url_for("booking_list"))
        return render_template("bookings/form.html", form=form, action="Edit")

    @app.route("/bookings/delete/<int:id>", methods=["POST"])
    def booking_delete(id):
        b = Booking.query.get_or_404(id)
        room = Room.query.get(b.room_id)
        room.room_status = 'Free'
        db.session.delete(b)
        db.session.commit()
        flash("Booking deleted", "success")
        return redirect(url_for("booking_list"))

    # ---------------- Services CRUD ----------------
    @app.route("/services")
    def service_list():
        services = Service.query.all()
        return render_template("services/list.html", services=services)

    @app.route("/services/add", methods=["GET", "POST"])
    def service_add():
        form = ServiceForm()
        if form.validate_on_submit():
            s = Service(name=form.name.data, description=form.description.data)
            db.session.add(s)
            db.session.commit()
            flash("Service added", "success")
            return redirect(url_for("service_list"))
        return render_template("services/form.html", form=form, action="Add")

    @app.route("/services/edit/<int:id>", methods=["GET", "POST"])
    def service_edit(id):
        s = Service.query.get_or_404(id)
        form = ServiceForm(obj=s)
        if form.validate_on_submit():
            s.name = form.name.data
            s.description = form.description.data
            db.session.commit()
            flash("Service updated", "success")
            return redirect(url_for("service_list"))
        return render_template("services/form.html", form=form, action="Edit")

    @app.route("/services/delete/<int:id>", methods=["POST"])
    def service_delete(id):
        s = Service.query.get_or_404(id)
        db.session.delete(s)
        db.session.commit()
        flash("Service deleted", "success")
        return redirect(url_for("service_list"))

    # ---------------- Staff CRUD ----------------
    @app.route("/staff")
    def staff_list():
        staff_members = Staff.query.all()
        return render_template("staff/list.html", staff=staff_members)

    @app.route("/staff/add", methods=["GET", "POST"])
    def staff_add():
        form = StaffForm()
        if form.validate_on_submit():
            st = Staff(fullname=form.fullname.data, contact=form.contact.data, role=form.role.data)
            db.session.add(st)
            db.session.commit()
            flash("Staff added", "success")
            return redirect(url_for("staff_list"))
        return render_template("staff/form.html", form=form, action="Add")

    @app.route("/staff/edit/<int:id>", methods=["GET", "POST"])
    def staff_edit(id):
        st = Staff.query.get_or_404(id)
        form = StaffForm(obj=st)
        if form.validate_on_submit():
            st.fullname = form.fullname.data
            st.contact = form.contact.data
            st.role = form.role.data
            db.session.commit()
            flash("Staff updated", "success")
            return redirect(url_for("staff_list"))
        return render_template("staff/form.html", form=form, action="Edit")

    @app.route("/staff/delete/<int:id>", methods=["POST"])
    def staff_delete(id):
        st = Staff.query.get_or_404(id)
        db.session.delete(st)
        db.session.commit()
        flash("Staff deleted", "success")
        return redirect(url_for("staff_list"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
