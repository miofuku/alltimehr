import { format, parseISO } from 'date-fns';

/**
 * Format date string to display format
 * @param dateString - ISO date string
 * @returns Formatted date string
 */
export const formatDate = (dateString: string): string => {
  try {
    return format(parseISO(dateString), 'MMM dd, yyyy HH:mm');
  } catch (error) {
    console.error('Invalid date format:', error);
    return dateString;
  }
};

/**
 * Check if date is in the past
 * @param date - Date to check
 * @returns boolean
 */
export const isPastDate = (date: Date): boolean => {
  return date < new Date();
}; 