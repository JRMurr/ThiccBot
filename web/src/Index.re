/* ReactDOMRe.renderToElementWithId(<DiscordServers/>, "servers"); */

/* ReactDOMRe.renderToElementWithId(<Component2 greeting="Hello!" />, "index2"); */

type page =
  | ServerList
  | Sever(string) /* server/id */
  | Error(string);

let int_of_string_opt = var =>
  switch (int_of_string(var)) {
  | int_var => Some(int_var)
  | exception (Failure("int_of_string")) => None
  };

module App = {
  type state = {route: page};
  type action =
    | UpdatePage(page);
  let component = ReasonReact.reducerComponent("App");
  let make = _children => {
    ...component,
    initialState: () => {route: ServerList},
    didMount: self => {
      let handle_url = (url: ReasonReact.Router.url) => {
        switch (url.path) {
        | ["server", id] =>
          /* switch (int_of_string_opt(id)) {
             | Some(x) => self.send(UpdatePage(Sever(x)))
             | None => self.send(UpdatePage(Error("Error parsing string id: (" ++ id ++ ")")))
             }; */
          self.send(UpdatePage(Sever(id)))
        | _ =>
          Js.log(url);
          self.send(UpdatePage(ServerList));
        };
      };
      /* handle inistal url for reloads */
      handle_url(ReasonReact.Router.dangerouslyGetInitialUrl());
      let watcherID = ReasonReact.Router.watchUrl(handle_url);
      self.onUnmount(() => ReasonReact.Router.unwatchUrl(watcherID));
    },
    reducer: (action, _state) =>
      switch (action) {
      | UpdatePage(route) => ReasonReact.Update({route: route})
      },
    render: ({state}) =>
      <div>
        {switch (state.route) {
         | ServerList => <DiscordServers />
         | Sever(id) => <ServerPage id />
         | Error(str) => <div> {ReasonReact.string(str)} </div>
         }}
      </div>,
  };
};
ReactDOMRe.renderToElementWithId(<App />, "app");