(function () {
    "use strict";

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function hasGsap() {
        return typeof window.gsap !== "undefined";
    }

    function playEntrance() {
        if (reduceMotion || !hasGsap()) {
            return;
        }

        // 页面入场只播放一次：先导航，再标题，最后聊天工作台。
        const timeline = window.gsap.timeline({
            defaults: {
                duration: 0.72,
                ease: "power3.out"
            }
        });

        timeline
            .from(".topbar", {
                y: -18,
                autoAlpha: 0,
                duration: 0.62
            })
            .from(".intro-copy > *", {
                y: 18,
                autoAlpha: 0,
                stagger: 0.1
            }, "-=0.28")
            .from(".intro-meta", {
                x: 18,
                autoAlpha: 0
            }, "-=0.48")
            .from(".chat-panel", {
                y: 32,
                autoAlpha: 0,
                scale: 0.992,
                duration: 0.88
            }, "-=0.48");
    }

    function animateMessage(messageElement) {
        if (!messageElement || reduceMotion || !hasGsap()) {
            return;
        }

        // 新消息只做一次轻微位移和淡入，避免长时间阅读时受到干扰。
        const isUser = messageElement.classList.contains("user");
        window.gsap.fromTo(
            messageElement,
            {
                x: isUser ? 14 : -14,
                y: 7,
                autoAlpha: 0,
                scale: 0.985
            },
            {
                x: 0,
                y: 0,
                autoAlpha: 1,
                scale: 1,
                duration: 0.42,
                ease: "power3.out",
                clearProps: "transform"
            }
        );
    }

    function animateClear(chatElement) {
        if (!chatElement || reduceMotion || !hasGsap()) {
            return;
        }

        // 清空后让空状态自然回到视线中，不使用夸张缩放。
        window.gsap.fromTo(
            chatElement.querySelector(".empty-state"),
            { y: 10, autoAlpha: 0 },
            { y: 0, autoAlpha: 1, duration: 0.46, ease: "power2.out" }
        );
    }

    function setupBackgroundVideo() {
        const background = document.querySelector(".ocean-background");
        const video = document.getElementById("ocean-video");

        if (!background || !video) {
            return;
        }

        const markReady = () => {
            background.classList.add("video-ready");
            background.classList.remove("video-error");
        };

        const markError = () => {
            background.classList.add("video-error");
            background.classList.remove("video-ready");
        };

        video.addEventListener("canplay", markReady, { once: true });
        video.addEventListener("error", markError, { once: true });

        if (video.readyState >= HTMLMediaElement.HAVE_FUTURE_DATA) {
            markReady();
        }

        const playPromise = video.play();
        if (playPromise && typeof playPromise.catch === "function") {
            playPromise.catch(markError);
        }
    }

    document.addEventListener("DOMContentLoaded", () => {
        setupBackgroundVideo();
        playEntrance();
    });

    window.oceanUI = {
        animateMessage,
        animateClear
    };
})();
