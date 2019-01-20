# runs a local web instance instead of in docker
pushd web/
npm run build
PORT=4000 npm run dev
popd
