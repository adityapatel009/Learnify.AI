// ==============================
// Learnify.AI - Clean JS version
// ==============================

// Smooth scroll to any section
function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: "smooth" });
}

// Handle Explore buttons
document.querySelectorAll(".explore-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const topic = btn.previousElementSibling.textContent.trim();
    const inputBox = document.querySelector("textarea[name='user_input']");
    if (inputBox) {
      inputBox.value = `I want to learn ${topic}`;
      scrollToSection("query");
    }
  });
});

// Loader hide after page load
window.addEventListener("load", () => {
  const loader = document.getElementById("loader");
  if (loader) loader.style.display = "none";
});

// ✨ Typing Effect
const text = "Empower your learning with AI.";
let i = 0;
function typeEffect() {
  const typing = document.getElementById("typing-text");
  if (!typing) return;
  if (i < text.length) {
    typing.textContent += text.charAt(i);
    i++;
    setTimeout(typeEffect, 70);
  }
}
window.addEventListener("load", typeEffect);

// ✨ Scroll reveal animation
const scrollElements = document.querySelectorAll(".scroll-reveal");
const revealOnScroll = () => {
  const triggerBottom = window.innerHeight * 0.9;
  scrollElements.forEach((el) => {
    const top = el.getBoundingClientRect().top;
    if (top < triggerBottom) el.classList.add("visible");
  });
};
window.addEventListener("scroll", revealOnScroll);
window.addEventListener("load", revealOnScroll);

// 🍔 Mobile menu toggle
const menuToggle = document.getElementById("menu-toggle");
const navLinks = document.querySelector(".nav-links");
if (menuToggle) {
  menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("active");
  });
}

// 🧭 Navbar scroll animation
window.addEventListener("scroll", () => {
  const navbar = document.querySelector(".navbar");
  if (window.scrollY > 30) navbar.classList.add("scrolled");
  else navbar.classList.remove("scrolled");
});
// 🌟 Quick Learn Carousel + Quotes
const slides = document.querySelectorAll(".slide");
const quotes = [
  "“The best way to predict the future is to invent it.”",
  "“Learning never exhausts the mind.”",
  "“An investment in knowledge pays the best interest.”",
  "“The expert in anything was once a beginner.”",
  "“Don’t watch the clock; do what it does. Keep going.”"
];

let slideIndex = 0;
let quoteIndex = 0;

function rotateSlides() {
  slides.forEach((s, i) => s.classList.toggle("active", i === slideIndex));
  slideIndex = (slideIndex + 1) % slides.length;
}
function rotateQuotes() {
  const quoteText = document.getElementById("quote-text");
  quoteText.style.opacity = 0;
  setTimeout(() => {
    quoteText.textContent = quotes[quoteIndex];
    quoteText.style.opacity = 1;
    quoteIndex = (quoteIndex + 1) % quotes.length;
  }, 400);
}

setInterval(rotateSlides, 3000);
setInterval(rotateQuotes, 5000);
