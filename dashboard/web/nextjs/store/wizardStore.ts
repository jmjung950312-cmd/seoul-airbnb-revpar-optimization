/* 마법사 입력 전역 상태 */

'use client'

import { create } from 'zustand'
import type { WizardState, HostType, RoomType } from '@/types/wizard'

interface WizardActions {
  setCurrentStep: (step: number) => void
  setHostType: (hostType: HostType) => void
  setDistrict: (district: string) => void
  setAddress: (address: string) => void
  setGeoLocation: (lat: number, lng: number, displayName: string) => void
  setRoomType: (roomType: RoomType) => void
  setAccommodates: (n: number) => void
  setBedrooms: (n: number) => void
  setBathrooms: (n: number) => void
  setAmenities: (amenities: string[]) => void
  toggleBookedDay: (day: number) => void
  setBookedDays: (days: Set<number>) => void
  setCalendarMonth: (year: number, month: number) => void
  updateStep2New: (data: Partial<WizardState['step2New']>) => void
  updateStep2Existing: (data: Partial<Omit<WizardState['step2Existing'], 'bookedDays'>>) => void
  updateStep3: (data: Partial<WizardState['step3']>) => void
  updateStep4: (data: Partial<WizardState['step4']>) => void
  reset: () => void
}

const today = new Date()

const initialState: WizardState = {
  currentStep: 1,
  step1: {
    hostType: null,
    district: '',
    address: '',
    geoLocation: null,
    roomType: 'Entire home/apt',
    propertyType: 'Apartment',
    accommodates: 2,
    bedrooms: 1,
    bathrooms: 1,
    amenities: ['wifi', 'kitchen'],
  },
  step2New: {
    targetAdr: 100000,
    targetOccupancy: 0.7,
    photos: 15,
    reviewScore: 4.8,
    responseRate: 0.95,
    instantBook: true,
  },
  step2Existing: {
    bookedDays: new Set<number>(),
    selectedYear: today.getFullYear(),
    selectedMonth: today.getMonth() + 1,
    currentAdr: 100000,
    reviewScore: 4.5,
    reviewCount: 0,
    responseRate: 0.9,
    photos: 10,
    instantBook: false,
  },
  step3: {
    cleaningFee: 30000,
    platformFee: 0.03,
    utilityMonthly: 100000,
    mortgageMonthly: 0,
    managementFee: 0,
    otherOpEx: 0,
  },
  step4: {
    minNights: 1,
    maxNights: 30,
    checkInWindow: '15:00-22:00',
    languages: ['ko'],
    petFriendly: false,
    smokingAllowed: false,
    partiesAllowed: false,
    selfCheckIn: true,
  },
}

export const useWizardStore = create<WizardState & WizardActions>()((set) => ({
  ...initialState,

  setCurrentStep: (step) => set({ currentStep: step }),

  setHostType: (hostType) =>
    set((s) => ({ step1: { ...s.step1, hostType } })),

  setDistrict: (district) =>
    set((s) => ({ step1: { ...s.step1, district } })),

  setAddress: (address) =>
    set((s) => ({ step1: { ...s.step1, address } })),

  setGeoLocation: (lat, lng, displayName) =>
    set((s) => ({ step1: { ...s.step1, geoLocation: { lat, lng, displayName } } })),

  setRoomType: (roomType) =>
    set((s) => ({ step1: { ...s.step1, roomType } })),

  setAccommodates: (n) =>
    set((s) => ({ step1: { ...s.step1, accommodates: n } })),

  setBedrooms: (n) =>
    set((s) => ({ step1: { ...s.step1, bedrooms: n } })),

  setBathrooms: (n) =>
    set((s) => ({ step1: { ...s.step1, bathrooms: n } })),

  setAmenities: (amenities) =>
    set((s) => ({ step1: { ...s.step1, amenities } })),

  toggleBookedDay: (day) =>
    set((s) => {
      const next = new Set(s.step2Existing.bookedDays)
      if (next.has(day)) next.delete(day)
      else next.add(day)
      return { step2Existing: { ...s.step2Existing, bookedDays: next } }
    }),

  setBookedDays: (days) =>
    set((s) => ({ step2Existing: { ...s.step2Existing, bookedDays: days } })),

  setCalendarMonth: (year, month) =>
    set((s) => ({
      step2Existing: { ...s.step2Existing, selectedYear: year, selectedMonth: month },
    })),

  updateStep2New: (data) =>
    set((s) => ({ step2New: { ...s.step2New, ...data } })),

  updateStep2Existing: (data) =>
    set((s) => ({ step2Existing: { ...s.step2Existing, ...data } })),

  updateStep3: (data) =>
    set((s) => ({ step3: { ...s.step3, ...data } })),

  updateStep4: (data) =>
    set((s) => ({ step4: { ...s.step4, ...data } })),

  reset: () => set(initialState),
}))
