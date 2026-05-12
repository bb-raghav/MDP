import { useState } from "react"

import PollutionMap from "../components/PollutionMap"

import "../styles/app.css"

export default function Dashboard() {

  const [selectedLayer, setSelectedLayer] =
    useState("SO2")

  const metrics = [
    {
      title: "NO₂ Layer",
      value: "Loaded",
      subtitle: "Satellite Raster",
    },

    {
      title: "SO₂ Layer",
      value: "Loaded",
      subtitle: "Feature Ready",
    },

    {
      title: "Raster Layers",
      value: "8",
      subtitle: "Processed",
    },

    {
      title: "Database",
      value: "Connected",
      subtitle: "Neon PostgreSQL",
    },
  ]

  const pipelineSteps = [
    "Satellite Raster Ingestion",
    "Feature Extraction",
    "Raster Alignment",
    "Dataset Generation",
    "ML Training Pipeline",
    "Interactive Heatmap",
  ]

  return (

    <div className="min-h-screen bg-black text-white p-10">

      {/* Header */}

      <div className="flex items-start justify-between mb-10">

        <div>

          <h1 className="text-5xl font-bold mb-3">
            AI/ML Air Quality Downscaling
          </h1>

          <p className="text-zinc-400 text-lg">
            Geospatial Environmental Intelligence Dashboard
          </p>

        </div>

        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl px-6 py-4">

          <p className="text-zinc-400 text-sm mb-1">
            Project Status
          </p>

          <p className="text-2xl font-bold text-green-400">
            Active
          </p>

        </div>

      </div>

      {/* Metrics */}

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-10">

        {metrics.map((metric, index) => (

          <div
            key={index}
            className="
              bg-zinc-900
              border border-zinc-800
              rounded-2xl
              p-6
            "
          >

            <p className="text-zinc-400 text-sm mb-3">
              {metric.title}
            </p>

            <h2 className="text-4xl font-bold mb-3">
              {metric.value}
            </h2>

            <p className="text-green-400 text-sm">
              {metric.subtitle}
            </p>

          </div>

        ))}

      </div>

      {/* Main Grid */}

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

        {/* Map Panel */}

        <div
          className="
            xl:col-span-2
            bg-zinc-900
            border border-zinc-800
            rounded-3xl
            p-6
          "
        >

          <div className="flex items-center justify-between mb-6">

            <h2 className="text-3xl font-bold">
              Pollution Layer Visualization
            </h2>

            <select
              value={selectedLayer}
              onChange={(e) =>
                setSelectedLayer(e.target.value)
              }
              className="
                bg-zinc-800
                border border-zinc-700
                rounded-xl
                px-4 py-2
                text-white
                outline-none
              "
            >

              <option value="SO2">SO₂</option>
              <option value="NO2">NO₂</option>
              <option value="CO">CO</option>
              <option value="NDVI">NDVI</option>

            </select>

          </div>

          <PollutionMap
            selectedLayer={selectedLayer}
          />

        </div>

        {/* Pipeline Panel */}

        <div
          className="
            bg-zinc-900
            border border-zinc-800
            rounded-3xl
            p-6
          "
        >

          <h2 className="text-3xl font-bold mb-8">
            Processing Pipeline
          </h2>

          <div className="space-y-5">

            {pipelineSteps.map((step, index) => (

              <div
                key={index}
                className="
                  flex items-center gap-4
                  bg-zinc-800
                  border border-zinc-700
                  rounded-2xl
                  p-4
                "
              >

                <div
                  className="
                    w-10 h-10
                    rounded-full
                    bg-green-500/20
                    border border-green-500
                    flex items-center justify-center
                    text-green-400
                    font-bold
                  "
                >
                  {index + 1}
                </div>

                <p className="text-lg">
                  {step}
                </p>

              </div>

            ))}

          </div>

        </div>

      </div>

    </div>
  )
}