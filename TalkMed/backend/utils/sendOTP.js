const nodemailer = require("nodemailer");

const sendOTP = async(email, otp) => {
    const transporter = nodemailer.createTransport({
        service: "gmail",
        auth: {
            user: process.env.EMAIL,
            pass: process.env.EMAIL_PASS,
        },
    });

    const mailOptions = {
        from: `"TalkMed OTP" <${process.env.EMAIL}>`,
        to: email,
        subject: "Your OTP for TalkMed Registration",
        html: `<h2>Your OTP is: ${otp}</h2>`,
    };

    try {
        await transporter.sendMail(mailOptions);
    } catch (error) {
        console.error("Error sending OTP email:", error);
        throw error;
    }
};

module.exports = sendOTP;
