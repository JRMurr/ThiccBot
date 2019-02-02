// Generated by BUCKLESCRIPT VERSION 4.0.18, PLEASE EDIT WITH CARE
'use strict';

var Block = require("bs-platform/lib/js/block.js");
var Curry = require("bs-platform/lib/js/curry.js");
var React = require("react");
var Belt_Array = require("bs-platform/lib/js/belt_Array.js");
var ReasonReact = require("reason-react/src/ReasonReact.js");
var ServerTypes$ReactTemplate = require("../Utils/ServerTypes.bs.js");
var DiscordServerCard$ReactTemplate = require("./DiscordServerCard.bs.js");

var component = ReasonReact.reducerComponent("DiscordServers");

function make(_children) {
  return /* record */[
          /* debugName */component[/* debugName */0],
          /* reactClassInternal */component[/* reactClassInternal */1],
          /* handedOffState */component[/* handedOffState */2],
          /* willReceiveProps */component[/* willReceiveProps */3],
          /* didMount */(function (self) {
              return Curry._1(self[/* send */3], /* ServerFetch */0);
            }),
          /* didUpdate */component[/* didUpdate */5],
          /* willUnmount */component[/* willUnmount */6],
          /* willUpdate */component[/* willUpdate */7],
          /* shouldUpdate */component[/* shouldUpdate */8],
          /* render */(function (self) {
              var match = self[/* state */1];
              if (typeof match === "number") {
                if (match !== 0) {
                  return React.createElement("div", undefined, "An error occurred!");
                } else {
                  return React.createElement("div", undefined, "Loading Severs...");
                }
              } else {
                return React.createElement("div", {
                            className: "container"
                          }, React.createElement("h1", undefined, "Servers"), Belt_Array.map(match[0], (function (server) {
                                  return ReasonReact.element(undefined, undefined, DiscordServerCard$ReactTemplate.make(server, /* array */[]));
                                })));
              }
            }),
          /* initialState */(function (_state) {
              return /* Loading */0;
            }),
          /* retainedProps */component[/* retainedProps */11],
          /* reducer */(function (action, _state) {
              if (typeof action === "number") {
                if (action !== 0) {
                  return /* Update */Block.__(0, [/* Error */1]);
                } else {
                  return /* UpdateWithSideEffects */Block.__(2, [
                            /* Loading */0,
                            (function (self) {
                                ServerTypes$ReactTemplate.ServerAPI[/* getServers */2](/* () */0).then((function (results) {
                                          Curry._1(self[/* send */3], /* ServersFetches */[results]);
                                          return Promise.resolve(/* () */0);
                                        })).catch((function (err) {
                                        console.log(err);
                                        return Promise.resolve(Curry._1(self[/* send */3], /* ServersFailedToFetch */1));
                                      }));
                                return /* () */0;
                              })
                          ]);
                }
              } else {
                return /* Update */Block.__(0, [/* Loaded */[action[0]]]);
              }
            }),
          /* jsElementWrapped */component[/* jsElementWrapped */13]
        ];
}

exports.component = component;
exports.make = make;
/* component Not a pure module */
