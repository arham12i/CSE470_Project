const Doctor = require("../models/Doctor");

const registerDoctor = async (req, res) => {
  try {
    const { name, specialization, phone, email, location } = req.body;

    if (!name || !specialization || !phone || !email || !location) {
      return res.status(400).json({ message: "All fields are required" });
    }

    const existingDoctor = await Doctor.findOne({ email });
    if (existingDoctor) {
      return res.status(400).json({ message: "Doctor already registered" });
    }

    const newDoctor = new Doctor({
      userId: req.user.id, 
      name,
      specialization,
      phone,
      email,
      location,
      verified: false,
    });

    await newDoctor.save();

    res.status(201).json({ message: "Doctor registered successfully, pending verification" });
  } catch (error) {
    console.error("Doctor registration error:", error);
    res.status(500).json({ message: "Server error" });
  }
};

const updateDoctorProfile = async (req, res) => {
  try {
    const doctorId = req.params.doctorId;
    const { name, specialization, phone, email, location } = req.body;

    const doctor = await Doctor.findById(doctorId);
    if (!doctor) return res.status(404).json({ message: "Doctor not found" });

    if (doctor.userId.toString() !== req.user.id && req.user.role !== "admin") {
      return res.status(403).json({ message: "Forbidden: You cannot update this profile" });
    }

    if (name) doctor.name = name;
    if (specialization) doctor.specialization = specialization;
    if (phone) doctor.phone = phone;
    if (email) doctor.email = email;
    if (location) doctor.location = location;

    await doctor.save();

    res.status(200).json({ message: "Doctor profile updated successfully", doctor });
  } catch (error) {
    console.error("Update doctor profile error:", error);
    res.status(500).json({ message: "Server error" });
  }
};

const getVerifiedDoctors = async (req, res) => {
  try {
    const verifiedDoctors = await Doctor.find({ verified: true });
    res.status(200).json(verifiedDoctors);
  } catch (error) {
    res.status(500).json({ message: "Server error", error });
  }
};

const getDoctorsByLocation = async (req, res) => {
  try {
    const location = req.params.location;

    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const skip = (page - 1) * limit;

    const locationRegex = new RegExp(`^${location}$`, "i");

    const doctors = await Doctor.find({ location: locationRegex, verified: true })
      .skip(skip)
      .limit(limit);

    const totalDoctors = await Doctor.countDocuments({ location: locationRegex, verified: true });

    res.status(200).json({
      page,
      limit,
      totalDoctors,
      totalPages: Math.ceil(totalDoctors / limit),
      doctors,
    });
  } catch (error) {
    res.status(500).json({ message: "Server error", error: error.message });
  }
};

const verifyDoctor = async (req, res) => {
  try {
    const { doctorId } = req.params;

    const doctor = await Doctor.findById(doctorId);
    if (!doctor) return res.status(404).json({ message: "Doctor not found" });

    if (doctor.verified) {
      return res.status(400).json({ message: "Doctor already verified" });
    }

    doctor.verified = true;
    await doctor.save();

    res.status(200).json({ message: "Doctor verified successfully" });
  } catch (error) {
    console.error("Doctor verification error:", error);
    res.status(500).json({ message: "Server error" });
  }
};

//Admin Use
const getAllDoctors = async (req, res) => {
  try {
    const doctors = await Doctor.find({});
    res.status(200).json(doctors);
  } catch (error) {
    console.error("Fetch all doctors error:", error);
    res.status(500).json({ message: "Server error" });
  }
};

module.exports = {
  getVerifiedDoctors,
  getDoctorsByLocation,
  registerDoctor,
  verifyDoctor,
  updateDoctorProfile,
  getAllDoctors,
};
