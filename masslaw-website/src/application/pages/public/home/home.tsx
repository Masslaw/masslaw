import React, {useEffect} from 'react';
import {ApplicationRoutes} from '../../../infrastructure/application_base/routing/application_routes';
import {NavigationFunctionState} from '../../../infrastructure/application_base/routing/application_global_routing';

import './css.css';
import {MasslawButton, MasslawButtonTypes} from '../../../shared/components/masslaw_button/masslaw_button';
import {ApplicationPage, ApplicationPageProps} from "../../../infrastructure/application_base/routing/application_page_renderer";
import {useGlobalState} from "../../../infrastructure/application_base/global_functionality/global_states";

export const Home: ApplicationPage = (props: ApplicationPageProps) => {

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    return (
        <>
            <header className={'landing-page-header'}>
                <div className={'landing-page-content-container'}>
                    <div className={'landing-header-logo'} />
                    <div className={'landing-text-container'}>
                        <h1 className={'landing-site-name'} style={{fontSize: '55px'}}>{'Masslaw'}</h1>
                        <p className={'landing-site-description'} style={{fontSize: '35px', marginTop: '15px'}}>{'For any case.'}</p>
                        <p className={'landing-site-catchphrase'} style={{fontSize: '20px', marginTop: '30px'}}>
                            {'A tool built for people that make law happen.'}
                        </p>
                    </div>
                    <div className={'landing-identity-buttons-container'}>
                        <div className={'landing-sign-up-button'}>
                            <MasslawButton
                                caption={'Sign Up'}
                                size={{w: 250, h: 50}}
                                onClick={e => {
                                    e.preventDefault();
                                    navigate_function(ApplicationRoutes.IDENTITY, {}, {'choose': 'signup'});
                                }}
                            />
                        </div>
                        <div className={'landing-already-have-an-account'}>{'Already have an account?'}</div>
                        <div className={'landing-log-in-button'}>
                            <MasslawButton
                                caption={'Log In'}
                                size={{w: 250, h: 50}}
                                buttonType={MasslawButtonTypes.SECONDARY}
                                onClick={e => {
                                    e.preventDefault();
                                    navigate_function(ApplicationRoutes.IDENTITY, {}, {'choose': 'login'});
                                }}
                            />
                        </div>
                    </div>
                </div>
            </header>
            <main className={'landing-page-main'}>
                <div className={'landing-page-content-container'} style={{height: "auto"}}>
                    <section className={'landing-content-region left'}>
                        <div
                            className={'landing-content-region-image i1'}
                        />
                        <div className={'landing-content-region-text'}>
                            Make your case files fully organized and ready to work with
                        </div>
                    </section>
                    <section className={'landing-content-region right'}>
                        <div
                            className={'landing-content-region-image i2'}
                        />
                        <div className={'landing-content-region-text'}>
                            Extract text from files that don't originally have it
                        </div>
                    </section>
                    <section className={'landing-content-region left'}>
                        <div
                            className={'landing-content-region-image i3'}
                        />
                        <div className={'landing-content-region-text'}>
                            Annotate and mark important sections of text in your case
                        </div>
                    </section>
                    <section className={'landing-content-region right'}>
                        <div
                            className={'landing-content-region-image i4'}
                        />
                        <div className={'landing-content-region-text'}>
                            Run text searches on your case's text to reach qualitative conclusions quickly
                        </div>
                    </section>
                    <section className={'landing-content-region left'}>
                        <div
                            className={'landing-content-region-image'}
                        />
                        <div className={'landing-content-region-text'}>
                            Summarize important ideas to go through them again easily
                        </div>
                    </section>
                    <section className={'landing-content-region right'}>
                        <div
                            className={'landing-content-region-image'}
                        />
                        <div className={'landing-content-region-text'}>
                            Share your cases with others to be able to work on them together
                        </div>
                    </section>
                    <section className={'landing-content-region left'}>
                        <div
                            className={'landing-content-region-image'}
                        />
                        <div className={'landing-content-region-text'}>
                            Let specialists view sections of your case to have their opinion
                        </div>
                    </section>
                    <section className={'landing-content-region right'}>
                        <div
                            className={'landing-content-region-image'}
                        />
                        <div className={'landing-content-region-text'}>
                            Be presented to AI generated conclusions about the case's content
                        </div>
                    </section>
                    <section className={'landing-content-region left'}>
                        <div
                            className={'landing-content-region-image'}
                        />
                        <div className={'landing-content-region-text'}>
                            View diagrams, and time lines that describe what happened in the case
                        </div>
                    </section>
                    <section className={'landing-content-region right'}>
                        <div
                            className={'landing-content-region-image'}
                        />
                        <div className={'landing-content-region-text'}>
                            View AI generated profiles for each of the case's subjects
                        </div>
                    </section>
                </div>
            </main>
            <footer className={'landing-page-footer'}>
                <div className={'landing-page-content-container'}>

                </div>
            </footer>
        </>
    );
}
