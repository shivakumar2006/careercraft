import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

const apiKey = import.meta.env.VITE_BACKEND_API_KEY;

export const api = createApi({
    reducerPath: "api",
    baseQuery: fetchBaseQuery({
        baseUrl: apiKey,
    }),

    tagTypes: ["Files"],

    endpoints: (builder) => ({
        analyze: builder.mutation({
            query: (data) => ({
                url: "/analyze",
                method: "POST",
                body: data,
            })
        }),

        getFiles: builder.query({
            query: () => ({
                url: "/files",
                method: "GET",
            }),
            providesTags: ["Files"]
        }),

        getFilesContent: builder.query({
            query: (filename) => ({
                url: `/files/${filename}`,
                method: "GET"
            }),
            providesTags: ["Files"]
        }),

        previewFile: builder.query({
            query: (filename) => `/preview/${filename}`,
        }),

        health: builder.query({
            query: () => "/health",
        }),
    }),
});

export const { useAnalyzeMutation, useGetFilesQuery, useGetFilesContentQuery, usePreviewFileQuery, useHealthQuery } = api;