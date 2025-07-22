const mongoose = require("mongoose");

const doctorSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  name: { type: String, required: true },
  specialization: { type: String, required: true },
  phone: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  location: { type: String, required: true },
  verified: { type: Boolean, default: false }
}, { timestamps: true });


module.exports = mongoose.model("Doctor", doctorSchema);