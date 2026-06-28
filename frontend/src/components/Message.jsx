export default function Message({ message, openSource }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      } mb-6`}
    >
      <div
        className={`max-w-3xl rounded-xl px-5 py-4 ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-slate-800 text-white"
        }`}
      >
        {/* Message */}
        <div className="whitespace-pre-wrap">
          {message.content}
        </div>

        {/* Sources */}
        {!isUser &&
          message.sources &&
          message.sources.length > 0 && (
            <div className="mt-5 border-t border-slate-600 pt-4">

              <div className="text-sm text-slate-400 mb-3 font-semibold">
                Sources
              </div>

              {message.sources.map((source, index) => (
                <button
                  key={index}
                  onClick={() => openSource(source)}
                  className="w-full text-left bg-slate-700 hover:bg-slate-600 rounded-lg p-4 mb-3 transition duration-200"
                >
                  <div className="font-semibold text-white">
                    📄 {source.filename}
                  </div>

                  <div className="text-xs text-slate-300 mt-1">
                    Page {source.page}
                  </div>

                  {source.excerpt && (
                    <div className="text-sm text-slate-200 mt-3 italic line-clamp-3">
                      "{source.excerpt}"
                    </div>
                  )}
                </button>
              ))}

            </div>
          )}
      </div>
    </div>
  );
}