import { configureStore } from '@reduxjs/toolkit'
import careerReducer from './careerSlice'
import { api } from './api'

export const store = configureStore({
    reducer: {
        career: careerReducer,
        [api.reducerPath]: api.reducer,
    },

    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(api.middleware),
})