import { configureStore } from '@reduxjs/toolkit'
import careerReducer from './careerSlice'

export const store = configureStore({
    reducer: { career: careerReducer }
})