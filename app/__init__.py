from quart import Quart
from quart_cors import cors
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import httpx
import asyncio

from app.core.config import config
from app.core.client import BMUClient

from app.modules.auth.routes import auth_bp
from app.modules.public.routes import public_bp
from app.modules.departments.routes import departments_bp
from app.modules.student.profile.routes import student_profile_bp
from app.modules.student.attendance.routes import student_attendance_bp
from app.modules.student.fees.routes import student_fees_bp
from app.modules.student.timetable.routes import student_timetable_bp
from app.modules.student.lms.routes import student_lms_bp
from app.modules.student.dashboard.routes import student_dashboard_bp

def create_app():
    app = Quart(__name__)
    app = cors(app, allow_origin="*")

    app.register_blueprint(auth_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(departments_bp)
    app.register_blueprint(student_profile_bp)
    app.register_blueprint(student_attendance_bp)
    app.register_blueprint(student_fees_bp)
    app.register_blueprint(student_timetable_bp)
    app.register_blueprint(student_lms_bp)
    app.register_blueprint(student_dashboard_bp)

    if config.APP_ENV == "production":
        scheduler = AsyncIOScheduler()

        async def keep_alive():
            """Ping the server itself to prevent sleeping on free tiers."""
            try:
                target_url = config.EXTERNAL_URL or "http://127.0.0.1:8000/"
                async with httpx.AsyncClient() as client:
                    await client.get(target_url)
                    logging.info("💓 Keep-alive ping sent.")
            except Exception as e:
                logging.warning(f"Keep-alive ping failed: {e}")

        scheduler.add_job(keep_alive, "interval", minutes=14)

    @app.route("/")
    async def root():
        return {"status": "running", "message": "BMU API is active 🚀"}

    @app.route("/health")
    async def health():
        return {"status": "healthy"}

    @app.before_serving
    async def startup():
        logging.info("🚀 Starting BMU API...")
        if config.APP_ENV == "production":
            scheduler.start()
            logging.info("⏰ Scheduler started for keep-alive pings.")

    @app.after_serving
    async def shutdown():
        logging.info("🛑 Shutting down BMU API...")
        await BMUClient.close()

    return app
