import { createSlice } from '@reduxjs/toolkit'

const careerSlice = createSlice({
    name: 'career',
    initialState: {
        logs: [],
        files: [],
        analysis: '',
        isRunning: false,
        isDone: false,
        error: null,
        activeFile: null,
        fileContent: '',
    },
    reducers: {
        addLog: (state, action) => { state.logs.push(action.payload) },
        setRunning: (state, action) => { state.isRunning = action.payload },
        setDone: (state, action) => {
            state.isDone = true
            state.isRunning = false
            state.files = action.payload.files
            state.analysis = action.payload.analysis
        },
        setError: (state, action) => {
            state.error = action.payload
            state.isRunning = false
        },
        setActiveFile: (state, action) => { state.activeFile = action.payload },
        setFileContent: (state, action) => { state.fileContent = action.payload },
        reset: (state) => {
            state.logs = []
            state.files = []
            state.analysis = ''
            state.isRunning = false
            state.isDone = false
            state.error = null
            state.activeFile = null
            state.fileContent = ''
        }
    }
})

export const {
    addLog, setRunning, setDone, setError,
    setActiveFile, setFileContent, reset
} = careerSlice.actions

export default careerSlice.reducer