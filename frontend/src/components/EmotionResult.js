//by Hridayansh, Riya, Ishita, Lokendra
import React from "react";
import PropTypes from "prop-types";

// Reusable MovieCard component
const MovieCard = ({ title, overview, poster }) => (
  <div className="bg-white shadow-lg rounded-2xl overflow-hidden transform hover:scale-[1.02] transition duration-300 ease-in-out">
    <img
      src={poster}
      alt={title}
      className="w-full aspect-[2/3] object-cover"
    />
    <div className="p-3">
      <h3 className="font-semibold text-base mb-1 text-gray-800 truncate">
        {title}
      </h3>
      <p className="text-xs text-gray-600 leading-snug">
        {overview.slice(0, 80)}...
      </p>
    </div>
  </div>
);

MovieCard.propTypes = {
  title: PropTypes.string.isRequired,
  overview: PropTypes.string.isRequired,
  poster: PropTypes.string.isRequired,
};

// Main EmotionResult component
const EmotionResult = ({ emotion, movies }) => {
  const hollywoodMovies = movies.filter((movie) => movie.original_language === "en");
  const bollywoodMovies = movies.filter((movie) => movie.original_language === "hi");

  return (
    <div className="mt-10 px-4 text-left w-full max-w-7xl mx-auto">
      <h2 className="text-3xl font-bold mb-10 tracking-tight text-center">
        Detected Emotion: <span className="capitalize text-indigo-600">{emotion}</span>
      </h2>

      {/* Hollywood Section */}
      {hollywoodMovies.length > 0 && (
        <section className="mb-10">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">🎬 Hollywood Movies</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
            {hollywoodMovies.map((movie) => (
              <MovieCard
                key={movie.id}
                title={movie.title}
                overview={movie.overview}
                poster={movie.poster}
              />
            ))}
          </div>
        </section>
      )}

      {/* Bollywood Section */}
      {bollywoodMovies.length > 0 && (
        <section className="mb-10">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">🎥 Bollywood Movies</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
            {bollywoodMovies.map((movie) => (
              <MovieCard
                key={movie.id}
                title={movie.title}
                overview={movie.overview}
                poster={movie.poster}
              />
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

// Prop Types for EmotionResult
EmotionResult.propTypes = {
  emotion: PropTypes.string.isRequired,
  movies: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      title: PropTypes.string.isRequired,
      overview: PropTypes.string.isRequired,
      poster: PropTypes.string.isRequired,
      original_language: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default EmotionResult;
