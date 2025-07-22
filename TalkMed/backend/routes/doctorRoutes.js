const express = require("express");
const router = express.Router();

const {
  getVerifiedDoctors,
  getDoctorsByLocation,
  registerDoctor,
  verifyDoctor,
  updateDoctorProfile,
  getAllDoctors

} = require("../controllers/doctorController");

const adminMiddlewares = require("../middlewares/adminMiddlewares");
const { protect } = require("../middlewares/authMiddlewares");

router.post("/register", registerDoctor);
router.patch("/verify/:doctorId", protect, adminMiddlewares, verifyDoctor);
router.patch("/update/:doctorId", protect, updateDoctorProfile);
router.get("/all", getAllDoctors);



module.exports = router;