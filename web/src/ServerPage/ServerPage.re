open Belt;
open ServerTypes;

type state =
  | Loading
  | Error
  | Loaded(discordServer);

type action =
  | ServerFetch
  | ServerFetched(discordServer)
  | ServersFailedToFetch;

let component = ReasonReact.reducerComponent("ServerPage");
let make = (~id: string, _children) => {
  ...component,
  initialState: _state => Loading,
  reducer: (action, _state) =>
    switch (action) {
    | ServerFetch =>
      ReasonReact.UpdateWithSideEffects(
        Loading,
        self => {
          let _ =
            ServerAPI.getServer(id)
            |> Js.Promise.then_(result => {
                 self.send(ServerFetched(result));
                 Js.Promise.resolve();
               })
            |> Js.Promise.catch(err => {
                 Js.log(err);
                 Js.Promise.resolve(self.send(ServersFailedToFetch));
               });
          ();
        },
      )
    | ServerFetched(server) => ReasonReact.Update(Loaded(server))
    | ServersFailedToFetch => ReasonReact.Update(Error)
    },
  didMount: self => self.send(ServerFetch),
  render: self =>
    switch (self.state) {
    | Error => <div> {ReasonReact.string("An error occurred!")} </div>
    | Loading => <div> {ReasonReact.string("Loading Sever...")} </div>
    | Loaded(server) =>
      <div className="container-fluid">
        <h1> {ReasonReact.string("Server: " ++ server.name)} </h1>
      </div>
    },
};