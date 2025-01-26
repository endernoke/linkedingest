export function isValidLinkedInId(userId) {
  if (!userId || userId.length < 3 || userId.length > 100) return false;

  // Check if contains at least one non-numeric character
  if (!/[^\d]/.test(userId)) return false;

  // Check for invalid hyphens (start, end, consecutive)
  if (userId.startsWith('-') || userId.endsWith('-') || /--/.test(userId)) return false;

  // Match valid characters: lowercase letters, numbers, hyphens, and CJK characters
  const validPattern = /^[a-z0-9\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f\u3131-\uD79D-]+$/;
  return validPattern.test(userId);
}