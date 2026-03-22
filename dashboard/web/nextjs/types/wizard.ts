/* 마법사 입력 관련 타입 정의 */

export type HostType = 'new' | 'existing'

export type RoomType = 'Entire home/apt' | 'Private room' | 'Shared room' | 'Hotel room'

export type PropertyType = 'Apartment' | 'House' | 'Guesthouse' | 'Boutique hotel' | 'Other'

export interface GeoLocation {
  lat: number
  lng: number
  displayName: string
}

export interface WizardStep1 {
  hostType: HostType | null
  district: string
  address: string
  geoLocation: GeoLocation | null
  roomType: RoomType
  propertyType: PropertyType
  accommodates: number
  bedrooms: number
  bathrooms: number
  amenities: string[]
}

export interface WizardStep2New {
  targetAdr: number
  targetOccupancy: number
  photos: number
  reviewScore: number
  responseRate: number
  instantBook: boolean
}

export interface WizardStep2Existing {
  bookedDays: Set<number>
  selectedYear: number
  selectedMonth: number
  currentAdr: number
  reviewScore: number
  reviewCount: number
  responseRate: number
  photos: number
  instantBook: boolean
}

export interface WizardStep3 {
  cleaningFee: number
  platformFee: number
  utilityMonthly: number
  mortgageMonthly: number
  managementFee: number
  otherOpEx: number
}

export interface WizardStep4 {
  minNights: number
  maxNights: number
  checkInWindow: string
  languages: string[]
  petFriendly: boolean
  smokingAllowed: boolean
  partiesAllowed: boolean
  selfCheckIn: boolean
}

export interface WizardState {
  currentStep: number
  step1: WizardStep1
  step2New: WizardStep2New
  step2Existing: WizardStep2Existing
  step3: WizardStep3
  step4: WizardStep4
}
