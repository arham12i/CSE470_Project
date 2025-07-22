const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },  
  email: { type: String, unique: true, required: true }, 
  phone: { type: String, required: true },    
  password: { type: String, required: true },    
  otp: String,
  otpExpiry: Date,
  isVerified: { type: Boolean, default: false },
  role: {
    type: String,
    enum: ["user", "doctor", "admin"],
    default: "user",
  },
  location: {
    city: { type: String, default: "" },
    area: { type: String, default: "" },
  },
  twoFAEnabled: {
  type: Boolean,
  default: false,
  },

});

module.exports = mongoose.model("User", userSchema);
