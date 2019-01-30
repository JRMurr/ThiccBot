/* ReactDOMRe.renderToElementWithId(<DiscordServers/>, "servers"); */

/* ReactDOMRe.renderToElementWithId(<Component2 greeting="Hello!" />, "index2"); */

type page =
  | ServerList

module App = {
  type state = {route: page};
  type action =
    | UpdatePage(page);
  let component = ReasonReact.reducerComponent("App");
  let make = _children => {
    ...component,
    initialState: () => {route: ServerList},
    reducer: (action, _state) =>
      switch (action) {
      | UpdatePage(route) => ReasonReact.Update({route: route})
      },
    render: ({state}) =>
      <div>
        (
          switch (state.route) {
          | ServerList => <DiscordServers/>
          }
        )
      </div>,
  };
};
ReactDOMRe.renderToElementWithId(<App/>, "app");