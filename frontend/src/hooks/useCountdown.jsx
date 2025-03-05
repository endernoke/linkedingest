import { useState, useEffect } from 'react';

function useCountdown(targetDate) {
  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft(targetDate));

  function calculateTimeLeft(targetTime) {
    const nowTime = new Date().getTime() / 1000;
    const difference = targetTime - nowTime;
    
    if (difference <= 0) {
      return null;
    }

    return {
      minutes: Math.floor((difference / 60) % 60),
      seconds: Math.floor(difference % 60)
    };
  }

  useEffect(() => {
    if (!targetDate) return;

    const timer = setInterval(() => {
      const calculated = calculateTimeLeft(targetDate);
      setTimeLeft(calculated);
      
      if (!calculated) {
        clearInterval(timer);
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [targetDate]);

  return timeLeft;
}

export default useCountdown;